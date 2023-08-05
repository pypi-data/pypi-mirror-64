class Deraser:
    """Deep Learning Model Compression Based on Weight Pruning"""

    def __init__(self, model_path: str, output_path: str = 'results',
                 pruning_factor: float = 0.5, base: str = 'pytorch'):
        """

        Parameters
        ----------
        model_path: Input model path.
        output_path: Output model path.
        pruning_factor: Pruning factor.
        base: Based framework. Either 'pytorch' or 'tensorflow'.
        """
        self.prune = None
        self.model_path = model_path
        self.output_path = output_path
        self.pruning_factor = pruning_factor

        if base == 'pytorch':
            self.prune = self.__run_pytorch
        elif base == 'tensorflow':
            self.prune = self.__run_tensorflow
        else:
            raise SyntaxError('Use either pytorch or tensorflow')

    def __run_pytorch(self):
        print('PyTorch is running.')
        print(self.model_path)

    def __run_tensorflow(self):
        print('TensorFlow is running.')
        print(self.model_path)


def test():
    de = Deraser('model_path', 'output_path')
    de.prune()


if __name__ == '__main__':
    test()
