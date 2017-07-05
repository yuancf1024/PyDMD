import numpy as np
import matplotlib.pyplot as plt

from dmd.dmdbase import DMDBase

class DMDExact(DMDBase):
	"""
	Dynamic Mode Decomposition

	This method decomposes

	:param numpy.ndarray X: the input matrix with dimension `m`x`n`
	:param int k: rank truncation in SVD
	"""
	def fit(self, X, Y=None):
		"""
		"""
		n_samples = X.shape[1]
		# split the data
		if Y is None:
			Y = X[:, 1:]
			X = X[:, :-1]

		#-----------------------------------------------------------------------
		# Singular Value Decomposition
		#-----------------------------------------------------------------------
		U, s, V = np.linalg.svd(X, full_matrices=False)
		V = np.conjugate(V.T)

		if self.svd_rank:
			U = U[:, 0:self.svd_rank]
			V = V[:, 0:self.svd_rank]
			s = s[0:self.svd_rank]

		Sinverse = np.diag(1. / s)

		#-----------------------------------------------------------------------
		# DMD Modes
		#-----------------------------------------------------------------------
		self._Atilde = np.transpose(U).dot(Y).dot(V).dot(Sinverse)
		self._basis = Y.dot(V).dot(Sinverse)
		self._eigs, self._mode_coeffs = np.linalg.eig(self._Atilde)

		self._modes = self._basis.dot(self._mode_coeffs)

		#-----------------------------------------------------------------------
		# DMD Amplitudes and Dynamics
		#-----------------------------------------------------------------------
		b = np.linalg.lstsq(self._modes, X[:, 0])[0]
		self._amplitudes = np.diag(b)

		self._vander = np.fliplr(np.vander(self._eigs, N=n_samples))

		return self
