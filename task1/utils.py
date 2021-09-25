'''
Utils file for task1
'''

taxRate = 0.10
importedTaxRate = 0.05

def st_getfile(filename):
    filename = "testinputs/"+filename+".txt"
    file = open(filename,'r')

    # splitting the input
    get_all_items = [line.strip().split(' at ') for line in file]
    file.close()

    return get_all_items

def st_get_itemtax(itemqty, itemtaxStatus, isitemimported, Price):
    itemPrice = float(Price)
    # getting the price by quantity
    itemPrice *= itemqty
    if itemtaxStatus :
        if isitemimported:
            # getting the price in total
            itemPrice += itemPrice * taxRate + itemPrice * importedTaxRate
            itemPrice = roundoff(itemPrice,itemtaxStatus, isitemimported)
            # getting the price after roundoff
            return itemPrice
        else:
            #  adding tax if item is tax applicable
            itemPrice += itemPrice * taxRate
            #getting the price
            itemPrice = roundoff(itemPrice,itemtaxStatus, isitemimported)
            return itemPrice
    else :
        # getting is item imported or not
        if isitemimported:
            # getting the price with imported tax rate add
            itemPrice += itemPrice * importedTaxRate
            # print "after import tax ", itemPrice
            itemPrice = roundoff(itemPrice,itemtaxStatus, isitemimported)
            # print "after round off ", itemPrice
            return itemPrice
        else :
            return itemPrice

file = open("testinputs/withoutax.txt", 'r')

# splitting the file
excluded_items = [line.strip() for line in file]

file.close()


def st_TaxStatus(getnameitem):
    taxApplied = True
    # getting the elements in tax excluded items
    for items in excluded_items:
        if(getnameitem.find(items)!=-1):
            # getting the tax applied
            taxApplied = False
            break

    if(getnameitem.find('imported')!=-1):
        isitemimported = True
    else:
        isitemimported = False

    if(taxApplied):
        if(isitemimported):
            # getting the tax if item is imported or not
            return True, True
        else:
            # getting the regular price of product
            return True, False
    else:
        if(isitemimported):
            return False, True
        else:
            return False, False


def roundoff(itemPrice, taxStatus, imported):
    # getting the roundoff
    Roundoff = 1 / 0.05
    itemnearestValue =  round((itemPrice*Roundoff)/Roundoff, 2)


    # performing roundoff value
    roundofflastDigit = int((itemnearestValue*100)%10)

    # get the value
    if roundofflastDigit == 0:
        return str(itemnearestValue)+'0'

    # round off to nearest 0.05
    if(roundofflastDigit >=1 and roundofflastDigit <5):
        # error in sales tax
        error = (5.0 - roundofflastDigit) /100
        itemnearestValue += error
    return str(itemnearestValue)