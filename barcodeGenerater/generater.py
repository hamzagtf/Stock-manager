from .setup import number_Of_Copies
from barcode import Code128
from barcode.writer import ImageWriter
from sql_db.db_sql import Connect_db
import random

def genrateBarCode(BARCODE):
    if len(BARCODE) > 0:
        image = Code128(BARCODE, writer=ImageWriter())
        image = image.save("default")
        return image



def generate_random_barcode():
	conn = Connect_db()

	num = random.randint(1, 13)
	_barcode = 1234567890123
	barcode = _barcode * num
	ref = True if conn.fecthRow('products', 'ref', f'ref="{barcode}"') else False
	if ref == False:
		return barcode

#print(generate_random_barcode())
