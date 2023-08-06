from xlrd import open_workbook

HEADERS = ['sn', 'product_name', 'category', 'sub_category', 'description', 'specification', 'total_variants', 'variants']

VARIANT_HEADERS = ['sku', 'mrp', 'fpo_price', 'farmer_price', 'minimum_order_quantity']

__all__ = ['XTProductJSON']

class XTProductJSON(object):
	"""open the workbook and read sheet1"""
	def __init__(self, path):
		'''
		path : excel sheet path
		ec = XTProductJSON("/home/swati/Downloads/Product Template.xlsx")
		'''
		super(XTProductJSON, self).__init__()
		self.loc = path
		self.wb = open_workbook(self.loc)
		self.sheet = self.wb.sheet_by_index(0)
		self.no_of_rows = self.sheet.nrows
		self.no_of_cols = self.sheet.ncols
		self.values = []

	def convert(self):
		# convert the excel sheet to list format
		self.values = []
		row = 1
		while row < self.no_of_rows:
		    col_value = {}
		    i = 0
		    col = 0
		    while col < self.no_of_cols:
		        value  = self.sheet.cell(row, col).value

		        if col == 5:
		        	value = value.split('\n')

		        elif col == 6:
		        	no_of_variants = int(value)
		        	col_value[HEADERS[i]] = no_of_variants
		        	i += 1
		        	variants = []
		        	col = col + 1
		        	
		        	for var in range(no_of_variants):
		        		variant = {}
		        		
		        		for k in range(5):
		        			v = self.sheet.cell(row, col).value
		        			variant[VARIANT_HEADERS[k]] = v
		        			col += 1
		        		
		        		if var < no_of_variants-1:
		        			row += 1

		        		col = 7

		        		variants.append(variant)
		        	value = variants
		        	col += 5 
		        
		        col_value[HEADERS[i]] = value
		        i += 1
		        col += 1
		    self.values.append(col_value)
		    row += 1
		return self.values
