class ModuleMixin:
    def predict(self, x):
        # Add a batch dim at the start converting x to 1 x (original dims)
        batch_of_one = x.unsqueeze(0)
        batch_of_one_y_hat = self.forward(batch_of_one)

        # Get rid of the batch dimensions
        y_hat = batch_of_one_y_hat.squeeze(0)
        return y_hat
