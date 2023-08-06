from typing import Tuple, Optional
import torch
import numpy as np
import SimpleITK as sitk
from ....utils import is_image_dict, check_consistent_shape
from ....torchio import LABEL, DATA, AFFINE, TYPE
from .. import Interpolation
from .. import RandomTransform


class RandomElasticDeformation(RandomTransform):
    """B-spline dense elastic deformation.

    Args:
        num_control_points:
        deformation_std:
        proportion_to_augment:
        image_interpolation:
        seed:
    """
    def __init__(
            self,
            num_control_points: int = 4,
            deformation_std: float = 15,
            proportion_to_augment: float = 1,
            image_interpolation: Interpolation = Interpolation.LINEAR,
            seed: Optional[int] = None,
            ):
        super().__init__(seed=seed)
        self._bspline_transformation = None
        self.num_control_points = max(num_control_points, 2)
        self.deformation_std = max(deformation_std, 1)
        self.proportion_to_augment = self.parse_probability(
            proportion_to_augment,
            'proportion_to_augment',
        )
        self.interpolation = self.parse_interpolation(image_interpolation)

    def apply_transform(self, sample: dict) -> dict:
        check_consistent_shape(sample)
        bspline_params = None
        sample['random_elastic_deformation'] = {}
        params_dict = sample['random_elastic_deformation']

        for image_dict in sample.values():
            if not is_image_dict(image_dict):
                continue
            if image_dict[TYPE] == LABEL:
                interpolation = Interpolation.NEAREST
            else:
                interpolation = self.interpolation
            if bspline_params is None:
                image = self.nib_to_sitk(
                    image_dict[DATA][0],
                    image_dict[AFFINE],
                )
                do_augmentation, bspline_params = self.get_params(
                    image,
                    self.num_control_points,
                    self.deformation_std,
                    self.proportion_to_augment,
                )
                params_dict['bspline_params'] = bspline_params
                params_dict['do_augmentation'] = int(do_augmentation)
                if not do_augmentation:
                    return sample
            image_dict[DATA] = self.apply_bspline_transform(
                image_dict[DATA],
                image_dict[AFFINE],
                bspline_params,
                interpolation,
            )
        return sample

    @staticmethod
    def get_params(
            image: sitk.Image,
            num_control_points: int,
            deformation_std: float,
            probability: float,
            ) -> Tuple:
        mesh_shape = 3 * (num_control_points,)
        bspline_transform = sitk.BSplineTransformInitializer(image, mesh_shape)
        default_params = bspline_transform.GetParameters()
        bspline_params = torch.rand(len(default_params))  # [0, 1)
        bspline_params -= 0.5  # [-0.5, 0.5)
        bspline_params *= deformation_std  # [-std/2, std/2)
        do_augmentation = torch.rand(1) < probability
        return do_augmentation, bspline_params.numpy()

    @staticmethod
    def get_bspline_transform(
            image: sitk.Image,
            num_control_points: int,
            bspline_params: np.ndarray,
            ) -> sitk.BSplineTransformInitializer:
        mesh_shape = 3 * (num_control_points,)
        bspline_transform = sitk.BSplineTransformInitializer(image, mesh_shape)
        bspline_transform.SetParameters(bspline_params.tolist())
        return bspline_transform

    def apply_bspline_transform(
            self,
            tensor: torch.Tensor,
            affine: np.ndarray,
            bspline_params: np.ndarray,
            interpolation: Interpolation,
            ) -> torch.Tensor:
        assert tensor.ndim == 4
        assert len(tensor) == 1
        image = self.nib_to_sitk(tensor[0], affine)
        floating = reference = image
        bspline_transform = self.get_bspline_transform(
            image,
            self.num_control_points,
            bspline_params,
        )
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(reference)
        resampler.SetTransform(bspline_transform)
        resampler.SetInterpolator(interpolation.value)
        resampler.SetDefaultPixelValue(tensor.min().item())
        resampler.SetOutputPixelType(sitk.sitkFloat32)
        resampled = resampler.Execute(floating)

        np_array = sitk.GetArrayFromImage(resampled)
        np_array = np_array.transpose()  # ITK to NumPy
        tensor[0] = torch.from_numpy(np_array)
        return tensor
