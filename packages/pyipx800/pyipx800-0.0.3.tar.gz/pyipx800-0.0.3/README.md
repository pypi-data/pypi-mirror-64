![PyPI](https://github.com/slashx57/pyipx800/workflows/Upload%20Python%20Package/badge.svg)

# pyipx800
Package Python pour contrôler le module IPX800v4 de GCE-Electronics.

## Utilisation

	from pyipx800 import pyipx800

	ipx = pyipx800.pyipx800("ipx800_v4", 80, "apikey")
	ipx.configure()

	d1 = ipx.inputs[0]
	print("Input %d : <%s> = %d" % (d1.id, d1.name, d1.state))



## License Information

[READ LICENSE FILE](LICENSE)

