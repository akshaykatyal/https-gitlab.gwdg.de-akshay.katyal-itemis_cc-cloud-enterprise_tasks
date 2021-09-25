from utils import st_getfile,st_get_itemtax,st_TaxStatus

while True:
    # getting the filename for the test input as there were three test input
    inputfilename = input('Enter name of \'inputfile with .txt format\'')
    print("\n")
    if inputfilename.lower()=='done':
        break
    # this is used to get all the items in filename
    get_all_items = st_getfile(inputfilename)

    # getting the tax and without tax product
    without_tax_items= 0
    with_tax_items = 0

    # traversing through the input file
    for item in get_all_items:
        # getting the quantity as input is at [0][0] place
        qty = int(item[0][0])
        # only some items has tax value so only with tax are added through this function
        itemtaxStatus, isitemimported = st_TaxStatus(item[0])
        st_itemTax = st_get_itemtax(qty, itemtaxStatus, isitemimported, item[1])
        without_tax_items += float(item[1])
        with_tax_items += float(st_itemTax)
        print(item[0], " : ", st_itemTax)

    get_sales_Tax = with_tax_items - without_tax_items
    # getting the sales tax value
    get_sales_Tax = format(get_sales_Tax, '.2f')
    st_with_tax = format(with_tax_items, '.2f')
    # this is the print format
    print("Sales Taxes: ", get_sales_Tax)

    print("Total: ", st_with_tax,"\n")
