def dictionary(word):
    dictionary={}
    print(word)
    # quantity
    dictionary.update(dict.fromkeys(
        ['sale', 'sales', 'abundance', 'batch', 'bulk', 'capacity', 'length', 'load', 'pile', 'profusion', 'total',
         'portion', 'quota', 'size', 'variety', 'volume', 'aggregate', 'allotment', 'amplitude', 'body', 'budget',
         'deal', 'expanse', 'extent', 'lot', 'magnitude', 'mass', 'measure', 'multitude', 'quantity', 'quantities'],
        "r.Quantity"))
    # price



    dictionary.update(dict.fromkeys(
        ['costliest', 'sum', 'amount', 'bill', 'cost', 'demand', 'discount', 'estimate', 'expenditure', 'expense',
         'fare', 'fee', 'figure', 'pay', 'payment', 'premium', 'rate', 'traffi', 'valuation', 'worth', 'appraisal',
         'assessment', 'barter', 'bounty', 'ceiling', 'charge', 'compensation', 'consideration', 'consideration',
         'damage', 'disbursement', 'dues', 'extraction', 'hire', 'outlay', 'prize', 'quotation', 'ransom',
         'reckoning', 'retail', 'reward', 'score', 'sticker', 'tab', 'ticket', 'toll', 'tune', 'wages', 'wholesale',
         'appraisement', 'asking price', 'face value', 'value', 'price', 'prices'], 'r.Price'))
    # products



    dictionary.update(dict.fromkeys(
        ['brand', 'commodity', 'crop', 'device', 'fruit', 'merchandise', 'output', 'produce', 'production',
         'profit', 'work', 'aftermath', 'artifact', 'blend', 'brew', 'by-product', 'compound', 'concoction',
         'confection', 'consequence', 'contrivance', 'creation', 'decoction', 'effect', 'emolument', 'fabrication',
         'gain', 'handiwork', 'invention', 'issue', 'legacy', 'line', 'manufacture', 'offshoot', 'outcome',
         'outgrowth', 'preparation', 'realization', 'result', 'synthetic', 'upshot', 'yield', 'spinoff', 'product',
         'products'], 's.Description'))
    # customers


    dictionary.update(dict.fromkeys(
        ['client', 'consumer', 'people', 'purchaser', 'patron', 'clientele', 'prospect', 'habitue', 'shopper',
         'buyers', 'customer', 'customers'], 'c.CustomerID'))
    # location


    dictionary.update(dict.fromkeys(
        ['country', 'countries', 'area', 'location', 'district', 'locale', 'neighborhood', 'part', 'point',
         'position', 'region', 'scene', 'section', 'site', 'situation', 'spot', 'station', 'venue', 'whereabouts',
         'bearings', 'fix', 'hole', 'locality', 'locus', 'post', 'tract', 'turf', 'location', 'locations'],
        'c.Country'))
    # revenue


    dictionary.update(dict.fromkeys(
        ['credit', 'dividend', 'earnings', 'fund', 'gain', 'interest', 'proceeds', 'receipt', 'returns', 'return',
         'salary', 'stock', 'wealth', 'yield', 'acquirement', 'annuity', 'emolument', 'fruits', 'gate', 'get',
         'gravy', 'handle', 'means', 'net', 'payoff', 'perquisite', 'resources', 'split', 'GDP', 'gross', 'revenue',
         'revenues'], 'r.revenue'))
    # print(dictionary)
    if word in dictionary.keys():
        return dictionary[word]

    else:
        return 

# print(dictionary('top'))

def chat_dict(word):
    mychat_dict={}
    #----------------------------------TOP---------------------------------------------------------------------#
    mychat_dict.update(dict.fromkeys(
        ["finest","greatest","top","foremost","leading","pre-eminent","premier","prime","first","chief","principal","supreme",
         "of the highest quality","superlative","unrivalled","second to none","without equal","nonpareil","unsurpassed",
          "unsurpassable","peerless","matchless","unparalleled","unbeaten","unbeatable","unexcelled","optimum","optimal",
          "ultimate","surpassing","incomparable","ideal","perfect","best"],
        "top"))

    #---------------------------------Bottom-------------------------------------------------------------------#
    mychat_dict.update(dict.fromkeys(
        ["base","basement","basic","ground","last","primary","radical","underlying","basal","foundational","lowermost","lowest",
        "nethermost","rock-bottom","undermost"], 'bottom'))
    
    #--------------------------------similar-------------------------------------------------------------------#
    mychat_dict.update(dict.fromkeys(
        ["alike","(much) the same","indistinguishable","close","near","almost identical","homogeneous","interchangeable",
        "kindred","akin","related","informalmuch of a muchness","comparable","like","corresponding","homogeneous","parallel",
        "equivalent","analogous","matching","like","much the same as","comparable to","close to","near","in the nature of"
        ], 'similar'))
    mychat_dict.update(dict.fromkeys(["help","helps","assist","corporate","corporates"],'Help'))
    mychat_dict.update(dict.fromkeys(["trends","growth","trend","flow","velocity of","function"],'trend'))
    mychat_dict.update(dict.fromkeys(["segment","segments","segmentation"],"segment"))
    if word in mychat_dict.keys():
        return mychat_dict[word]

    else:
        return