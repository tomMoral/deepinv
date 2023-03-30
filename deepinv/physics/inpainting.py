from deepinv.physics.forward import DecomposablePhysics
import torch


class Inpainting(DecomposablePhysics):
    r'''

    Inpainting forward operator, keeps a subset of entries.

    The operator is described by the diagonal matrix

    .. math::

        A = \text{diag}(m) \in \mathbb{R}^{n\times n}

    where :math:`m` is a binary mask with n entries.

    This operator is linear and has a trivial SVD decomposition, which allows for fast computation of the pseudoinverse and proximal operator.

    :param tuple tensor_size: size of the input images, e.g., (C, H, W).
    :param torch.tensor, float mask: If the input is a float, the entries of the mask will be sampled from a bernoulli distribution with probability=mask. If the input is a torch tensor matching tensor_size, the mask will be set to this tensor.

    '''
    def __init__(self, tensor_size, mask=0.3, device='cpu', **kwargs):
        super().__init__(**kwargs)
        self.tensor_size = tensor_size

        if isinstance(mask, torch.Tensor):# check if the user created mask
            self.mask = mask
        else:# otherwise create new random mask
            mask_rate = mask
            self.mask = torch.ones(tensor_size, device=device)
            self.mask[torch.rand_like(self.mask) > mask_rate] = 0

        self.mask = torch.nn.Parameter(self.mask.unsqueeze(0), requires_grad=False)
