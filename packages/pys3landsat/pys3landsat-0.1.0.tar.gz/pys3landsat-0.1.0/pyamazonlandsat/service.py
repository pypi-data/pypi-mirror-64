import attr

from pyamazonlandsat.product import Product


@attr.s
class Service:
    """Main class. Whole interaction with the module
    must be from here.

    :param name: name of the product to download. Following
    the Landsat standard name.
    ;type name: str
    :param output_path: ouput path whre save the Product
    downloaded.
    :type output_path: str.
    """
    name = attr.ib()
    output_path = attr.ib()

    def get_product(self):
        """Get the Product according to `name`.

        This method get  download the product with name `name`
        and save on `output_path`
        """
        product = Product(self.name, self.output_path)
        product.get_image_product()

