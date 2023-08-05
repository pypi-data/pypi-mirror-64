from jijcloud.sampler import JijCloudSampler
from jijcloud.sampler.model_post import JijModelSamplerInterface


class JijSASampler(JijCloudSampler, JijModelSamplerInterface):
    hardware = 'cpu'
    algorithm = 'sa'

    def sample(self, bqm,
               beta_min=None, beta_max=None,
               num_reads=1, mc_steps=100):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            mc_steps (int, optional): number of MonteCarlo steps.

        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        return super().sample(
            bqm, num_reads, mc_steps,
            beta_min=beta_min, beta_max=beta_max,
        )

    def sample_model(self, model, conditions, multipliers, vartype='BINARY',
                     feed_dict=None,
                     search=None,
                     max_iter=5,
                     beta_min=None, beta_max=None,
                     num_reads=1, mc_steps=100
                     ):
        """sample model
        Args:
            model (obj): PyQUBO compiled model.
            conditions (dict): conditios.
            multipliers (dict): key: multiplier's label, value: 
            vartype (str): variable type.  
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            mc_steps (int, optional): number of MonteCarlo steps.

        Returns:
            dimod.SampleSet: store minimum energy samples
                            .info['energy'] store all sample energies
        """
        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')
        return super().sample_model(model, conditions, multipliers, vartype,
                                    feed_dict=feed_dict,
                                    search=search,
                                    max_iter=max_iter,
                                    beta_min=beta_min, beta_max=beta_max,
                                    num_reads=num_reads, mc_steps=mc_steps)
