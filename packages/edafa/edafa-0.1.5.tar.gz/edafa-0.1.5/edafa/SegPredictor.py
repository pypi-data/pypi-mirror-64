from .BasePredictor import BasePredictor
import numpy as np
from .utils import *

class SegPredictor(BasePredictor):
	def __init__(self,in_patch_size,out_channels,conf,out_patch_size=None):
		"""
		Initialize class
		
		:param in_patch_size: input patch size (assumes width = height)
		:param out_channels: number of channels in your model's output (for example number of classes in segmentation)
		:param conf: configuration (json string or file path)
		:param out_patch_size: output patch size in case of no padding (default = in_patch_size)

		"""
		super().__init__(conf=conf)

		self.in_patch_size = in_patch_size	
		self.out_channels = out_channels

		if out_patch_size is None:
			self.out_patch_size = self.in_patch_size
		else:
			self.out_patch_size = out_patch_size


	def reverse_aug(self,aug_patch):
		"""
		Reverse augmentations applied and calculate their combined mean

		:param aug_patch: set of prediction of the model to different augmentations
		
		:returns: single combined patch 
		"""
		if self.mean == "ARITH":
			mixed = np.zeros(aug_patch.shape[1:])
			for i,aug in enumerate(self.augs):
				mixed += reverse(aug,aug_patch[i])
			return mixed / len(self.augs)
		elif self.mean == "GEO":
			mixed = np.ones(aug_patch.shape[1:])
			for i,aug in enumerate(self.augs):
				mixed *= reverse(aug,aug_patch[i])
			return mixed ** (1./len(self.augs))


	def _predict_single(self,img,overlap=0):
		"""
		predict single image
		
		:param img: image to predict
		:param overlap: overlap size between patches in prediction of large image (default = 0)

		:return: prediction on the image
		"""
		h,w = img.shape[:2]
		output = np.zeros((h,w,self.out_channels))
		times = np.zeros(img.shape[:2])

		img = add_reflections(img,self.in_patch_size,self.out_patch_size)

		padding = rint((self.in_patch_size - self.out_patch_size)/2.)

		delta = self.in_patch_size-overlap

		in_patch_h = min(img.shape[0],self.in_patch_size)
		in_patch_w = min(img.shape[1],self.in_patch_size)

		for h in range(0,img.shape[0]-in_patch_h +1,delta):
			for w in range(0,img.shape[1]-in_patch_w +1,delta):
				in_patch = img[h:(h+in_patch_h),
								w:(w+in_patch_w),
								:]
				aug_patches = self.apply_aug(in_patch)
				pred = self.predict_patches(aug_patches)
				pred = self.reverse_aug(pred)

				output[padding:(padding+self.out_patch_size),
						padding:(padding+self.out_patch_size),
						:] = pred

				times[padding:(padding+self.out_patch_size),
						padding:(padding+self.out_patch_size)] += 1
		
		return (output/times[:,:,np.newaxis])

