def ClearQuery(query):
	t = query.lower()
	t = re.sub(u'[^a-zA-Z0-9абвгдеёжзийклмнопрстуфхцшщыъьэючя\s.-]',' ',t)
	words = t.split(' ')
	wordsList = []
	for word in words:
		if '.' in word:
			if re.match(u'^(\d)+.(\d)+$',word):
				wordsList.append(word)
			else:
				wordsList.append(word.replace('.',' '))
		else:
			wordsList.append(word)
	t = ' '.join(wordsList)
	t = ' '.join(t.split())
	t = t.replace(' - ', '-')
	t = t.replace(' -','-')
	t = t.replace('- ','-')
	t = t.replace(u'б у',u'бу')
	t = t.replace(u'ж к',u'жк')
	t = t.replace(u'ё',u'е')
	return t

def CleanStopWords (query):
	pattern = u'(^и\s|\sи\s|\sи$|^и$|^в\s|\sв\s|\sв$|^в$|^я\s|\sя\s|\sя$|^я$|^с\s|\sс\s|\sс$|^с$|^а\s|\sа\s|\sа$|^а$|^к\s|\sк\s|\sк$|^к$|^у\s|\sу\s|\sу$|^у$|^о\s|\sо\s|\sо$|^о$|^не\s|\sне\s|\sне$|^не$|^он\s|\sон\s|\sон$|^он$|^на\s|\sна\s|\sна$|^на$|^по\s|\sпо\s|\sпо$|^по$|^но\s|\sно\s|\sно$|^но$|^ты\s|\sты\s|\sты$|^ты$|^из\s|\sиз\s|\sиз$|^из$|^мы\s|\sмы\s|\sмы$|^мы$|^за\s|\sза\s|\sза$|^за$|^вы\s|\sвы\s|\sвы$|^вы$|^же\s|\sже\s|\sже$|^же$|^от\s|\sот\s|\sот$|^от$|^бы\s|\sбы\s|\sбы$|^бы$|^да\s|\sда\s|\sда$|^да$|^до\s|\sдо\s|\sдо$|^до$|^во\s|\sво\s|\sво$|^во$|^об\s|\sоб\s|\sоб$|^об$|^ко\s|\sко\s|\sко$|^ко$|^что\s|\sчто\s|\sчто$|^что$|^тот\s|\sтот\s|\sтот$|^тот$|^это\s|\sэто\s|\sэто$|^это$|^как\s|\sкак\s|\sкак$|^как$|^она\s|\sона\s|\sона$|^она$|^они\s|\sони\s|\sони$|^они$|^так\s|\sтак\s|\sтак$|^так$|^еще\s|\sеще\s|\sеще$|^еще$|^уже\s|\sуже\s|\sуже$|^уже$|^для\s|\sдля\s|\sдля$|^для$|^вот\s|\sвот\s|\sвот$|^вот$|^кто\s|\sкто\s|\sкто$|^кто$|^мой\s|\sмой\s|\sмой$|^мой$|^или\s|\sили\s|\sили$|^или$|^нет\s|\sнет\s|\sнет$|^нет$|^наш\s|\sнаш\s|\sнаш$|^наш$|^сам\s|\sсам\s|\sсам$|^сам$|^чем\s|\sчем\s|\sчем$|^чем$|^при\s|\sпри\s|\sпри$|^при$|^оно\s|\sоно\s|\sоно$|^оно$|^быть\s|\sбыть\s|\sбыть$|^быть$|^весь\s|\sвесь\s|\sвесь$|^весь$|^этот\s|\sэтот\s|\sэтот$|^этот$|^мочь\s|\sмочь\s|\sмочь$|^мочь$|^один\s|\sодин\s|\sодин$|^один$|^себя\s|\sсебя\s|\sсебя$|^себя$|^свое\s|\sсвое\s|\sсвое$|^свое$|^если\s|\sесли\s|\sесли$|^если$|^свой\s|\sсвой\s|\sсвой$|^свой$|^есть\s|\sесть\s|\sесть$|^есть$|^такой\s|\sтакой\s|\sтакой$|^такой$|^когда\s|\sкогда\s|\sкогда$|^когда$|^чтобы\s|\sчтобы\s|\sчтобы$|^чтобы$|^только\s|\sтолько\s|\sтолько$|^только$|^тебя\s|\sтебя\s|\sтебя$|^тебя$|^тебе\s|\sтебе\s|\sтебе$|^тебе$|^тобой\s|\sтобой\s|\sтобой$|^тобой$|^вас\s|\sвас\s|\sвас$|^вас$|^вам\s|\sвам\s|\sвам$|^вам$|^вами\s|\sвами\s|\sвами$|^вами$|^нас\s|\sнас\s|\sнас$|^нас$|^нам\s|\sнам\s|\sнам$|^нам$|^нами\s|\sнами\s|\sнами$|^нами$|^чего\s|\sчего\s|\sчего$|^чего$|^чему\s|\sчему\s|\sчему$|^чему$|^того\s|\sтого\s|\sтого$|^того$|^тому\s|\sтому\s|\sтому$|^тому$|^тем\s|\sтем\s|\sтем$|^тем$|^том\s|\sтом\s|\sтом$|^том$|^те\s|\sте\s|\sте$|^те$|^тех\s|\sтех\s|\sтех$|^тех$|^теми\s|\sтеми\s|\sтеми$|^теми$|^этого\s|\sэтого\s|\sэтого$|^этого$|^этому\s|\sэтому\s|\sэтому$|^этому$|^этим\s|\sэтим\s|\sэтим$|^этим$|^этом\s|\sэтом\s|\sэтом$|^этом$|^этих\s|\sэтих\s|\sэтих$|^этих$|^эти\s|\sэти\s|\sэти$|^эти$|^этими\s|\sэтими\s|\sэтими$|^этими$|^ее\s|\sее\s|\sее$|^ее$|^ей\s|\sей\s|\sей$|^ей$|^ней\s|\sней\s|\sней$|^ней$|^них\s|\sних\s|\sних$|^них$|^кого\s|\sкого\s|\sкого$|^кого$|^кому\s|\sкому\s|\sкому$|^кому$|^кем\s|\sкем\s|\sкем$|^кем$|^ком\s|\sком\s|\sком$|^ком$|^моего\s|\sмоего\s|\sмоего$|^моего$|^моему\s|\sмоему\s|\sмоему$|^моему$|^моим\s|\sмоим\s|\sмоим$|^моим$|^моем\s|\sмоем\s|\sмоем$|^моем$|^мои\s|\sмои\s|\sмои$|^мои$|^моих\s|\sмоих\s|\sмоих$|^моих$|^моими\s|\sмоими\s|\sмоими$|^моими$|^нашего\s|\sнашего\s|\sнашего$|^нашего$|^нашему\s|\sнашему\s|\sнашему$|^нашему$|^нашим\s|\sнашим\s|\sнашим$|^нашим$|^нашем\s|\sнашем\s|\sнашем$|^нашем$|^наших\s|\sнаших\s|\sнаших$|^наших$|^нашими\s|\sнашими\s|\sнашими$|^нашими$|^самим\s|\sсамим\s|\sсамим$|^самим$|^сами\s|\sсами\s|\sсами$|^сами$|^самих\s|\sсамих\s|\sсамих$|^самих$|^самими\s|\sсамими\s|\sсамими$|^самими$|^был\s|\sбыл\s|\sбыл$|^был$|^была\s|\sбыла\s|\sбыла$|^была$|^было\s|\sбыло\s|\sбыло$|^было$|^были\s|\sбыли\s|\sбыли$|^были$|^буду\s|\sбуду\s|\sбуду$|^буду$|^будешь\s|\sбудешь\s|\sбудешь$|^будешь$|^будет\s|\sбудет\s|\sбудет$|^будет$|^будем\s|\sбудем\s|\sбудем$|^будем$|^будете\s|\sбудете\s|\sбудете$|^будете$|^будут\s|\sбудут\s|\sбудут$|^будут$|^всего\s|\sвсего\s|\sвсего$|^всего$|^всему\s|\sвсему\s|\sвсему$|^всему$|^всем\s|\sвсем\s|\sвсем$|^всем$|^всех\s|\sвсех\s|\sвсех$|^всех$|^все\s|\sвсе\s|\sвсе$|^все$|^всеми\s|\sвсеми\s|\sвсеми$|^всеми$|^могу\s|\sмогу\s|\sмогу$|^могу$|^можешь\s|\sможешь\s|\sможешь$|^можешь$|^может\s|\sможет\s|\sможет$|^может$|^можем\s|\sможем\s|\sможем$|^можем$|^можете\s|\sможете\s|\sможете$|^можете$|^мог\s|\sмог\s|\sмог$|^мог$|^могла\s|\sмогла\s|\sмогла$|^могла$|^могли\s|\sмогли\s|\sмогли$|^могли$|^моги\s|\sмоги\s|\sмоги$|^моги$|^могите\s|\sмогите\s|\sмогите$|^могите$|^одного\s|\sодного\s|\sодного$|^одного$|^одному\s|\sодному\s|\sодному$|^одному$|^одним\s|\sодним\s|\sодним$|^одним$|^одном\s|\sодном\s|\sодном$|^одном$|^одних\s|\sодних\s|\sодних$|^одних$|^одни\s|\sодни\s|\sодни$|^одни$|^одними\s|\sодними\s|\sодними$|^одними$|^себе\s|\sсебе\s|\sсебе$|^себе$|^собой\s|\sсобой\s|\sсобой$|^собой$|^собою\s|\sсобою\s|\sсобою$|^собою$|^своего\s|\sсвоего\s|\sсвоего$|^своего$|^своему\s|\sсвоему\s|\sсвоему$|^своему$|^своим\s|\sсвоим\s|\sсвоим$|^своим$|^своем\s|\sсвоем\s|\sсвоем$|^своем$|^своих\s|\sсвоих\s|\sсвоих$|^своих$|^свои\s|\sсвои\s|\sсвои$|^свои$|^своими\s|\sсвоими\s|\sсвоими$|^своими$|^такого\s|\sтакого\s|\sтакого$|^такого$|^такому\s|\sтакому\s|\sтакому$|^такому$|^таким\s|\sтаким\s|\sтаким$|^таким$|^таком\s|\sтаком\s|\sтаком$|^таком$|^таких\s|\sтаких\s|\sтаких$|^таких$|^такие\s|\sтакие\s|\sтакие$|^такие$|^такими\s|\sтакими\s|\sтакими$|^такими$|^который\s|\sкоторый\s|\sкоторый$|^который$|^которого\s|\sкоторого\s|\sкоторого$|^которого$|^которому\s|\sкоторому\s|\sкоторому$|^которому$|^которым\s|\sкоторым\s|\sкоторым$|^которым$|^котором\s|\sкотором\s|\sкотором$|^котором$|^которые\s|\sкоторые\s|\sкоторые$|^которые$|^которых\s|\sкоторых\s|\sкоторых$|^которых$|^которыми\s|\sкоторыми\s|\sкоторыми$|^которыми$|^меня\s|\sменя\s|\sменя$|^меня$|^мне\s|\sмне\s|\sмне$|^мне$|^мной\s|\sмной\s|\sмной$|^мной$|^чём\s|\sчём\s|\sчём$|^чём$|^её\s|\sеё\s|\sеё$|^её$|^моём\s|\sмоём\s|\sмоём$|^моём$|^самого\s|\sсамого\s|\sсамого$|^самого$|^самому\s|\sсамому\s|\sсамому$|^самому$|^самом\s|\sсамом\s|\sсамом$|^самом$|^всём\s|\sвсём\s|\sвсём$|^всём$|^могло\s|\sмогло\s|\sмогло$|^могло$|^своё\s|\sсвоё\s|\sсвоё$|^своё$|^своём\s|\sсвоём\s|\sсвоём$|^своём$|^ем\s|\sем\s|\sем$|^ем$|^их\s|\sих\s|\sих$|^их$|^им\s|\sим\s|\sим$|^им$|^то\s|\sто\s|\sто$|^то$|^та\s|\sта\s|\sта$|^та$|^ту\s|\sту\s|\sту$|^ту$|^ею\s|\sею\s|\sею$|^ею$|^ел\s|\sел\s|\sел$|^ел$|^его\s|\sего\s|\sего$|^его$|^мою\s|\sмою\s|\sмою$|^мою$|^нею\s|\sнею\s|\sнею$|^нею$|^ест\s|\sест\s|\sест$|^ест$|^ешь\s|\sешь\s|\sешь$|^ешь$|^ела\s|\sела\s|\sела$|^ела$|^тою\s|\sтою\s|\sтою$|^тою$|^оне\s|\sоне\s|\sоне$|^оне$|^имъ\s|\sимъ\s|\sимъ$|^имъ$|^этой\s|\sэтой\s|\sэтой$|^этой$|^свою\s|\sсвою\s|\sсвою$|^свою$|^него\s|\sнего\s|\sнего$|^него$|^одна\s|\sодна\s|\sодна$|^одна$|^всей\s|\sвсей\s|\sвсей$|^всей$|^одно\s|\sодно\s|\sодно$|^одно$|^наши\s|\sнаши\s|\sнаши$|^наши$|^ними\s|\sними\s|\sними$|^ними$|^сама\s|\sсама\s|\sсама$|^сама$|^одну\s|\sодну\s|\sодну$|^одну$|^нему\s|\sнему\s|\sнему$|^нему$|^моей\s|\sмоей\s|\sмоей$|^моей$|^наша\s|\sнаша\s|\sнаша$|^наша$|^само\s|\sсамо\s|\sсамо$|^само$|^будь\s|\sбудь\s|\sбудь$|^будь$|^наше\s|\sнаше\s|\sнаше$|^наше$|^нашу\s|\sнашу\s|\sнашу$|^нашу$|^мною\s|\sмною\s|\sмною$|^мною$|^своя\s|\sсвоя\s|\sсвоя$|^своя$|^саму\s|\sсаму\s|\sсаму$|^саму$|^всея\s|\sвсея\s|\sвсея$|^всея$|^едят\s|\sедят\s|\sедят$|^едят$|^моею\s|\sмоею\s|\sмоею$|^моею$|^всею\s|\sвсею\s|\sвсею$|^всею$|^едим\s|\sедим\s|\sедим$|^едим$|^этою\s|\sэтою\s|\sэтою$|^этою$|^могут\s|\sмогут\s|\sмогут$|^могут$|^своей\s|\sсвоей\s|\sсвоей$|^своей$|^одной\s|\sодной\s|\sодной$|^одной$|^такое\s|\sтакое\s|\sтакое$|^такое$|^такая\s|\sтакая\s|\sтакая$|^такая$|^нашей\s|\sнашей\s|\sнашей$|^нашей$|^такую\s|\sтакую\s|\sтакую$|^такую$|^тобою\s|\sтобою\s|\sтобою$|^тобою$|^своею\s|\sсвоею\s|\sсвоею$|^своею$|^томах\s|\sтомах\s|\sтомах$|^томах$|^такою\s|\sтакою\s|\sтакою$|^такою$|^комья\s|\sкомья\s|\sкомья$|^комья$|^будучи\s|\sбудучи\s|\sбудучи$|^будучи$|^будьте\s|\sбудьте\s|\sбудьте$|^будьте$|^которая\s|\sкоторая\s|\sкоторая$|^которая$|^которой\s|\sкоторой\s|\sкоторой$|^которой$|^которое\s|\sкоторое\s|\sкоторое$|^которое$|^которую\s|\sкоторую\s|\sкоторую$|^которую$|^емъ\s|\sемъ\s|\sемъ$|^емъ$|^a\s|\sa\s|\sa$|^a$|^i\s|\si\s|\si$|^i$|^be\s|\sbe\s|\sbe$|^be$|^of\s|\sof\s|\sof$|^of$|^in\s|\sin\s|\sin$|^in$|^to\s|\sto\s|\sto$|^to$|^it\s|\sit\s|\sit$|^it$|^on\s|\son\s|\son$|^on$|^do\s|\sdo\s|\sdo$|^do$|^at\s|\sat\s|\sat$|^at$|^we\s|\swe\s|\swe$|^we$|^by\s|\sby\s|\sby$|^by$|^or\s|\sor\s|\sor$|^or$|^as\s|\sas\s|\sas$|^as$|^if\s|\sif\s|\sif$|^if$|^my\s|\smy\s|\smy$|^my$|^so\s|\sso\s|\sso$|^so$|^me\s|\sme\s|\sme$|^me$|^no\s|\sno\s|\sno$|^no$|^am\s|\sam\s|\sam$|^am$|^the\s|\sthe\s|\sthe$|^the$|^and\s|\sand\s|\sand$|^and$|^for\s|\sfor\s|\sfor$|^for$|^you\s|\syou\s|\syou$|^you$|^but\s|\sbut\s|\sbut$|^but$|^not\s|\snot\s|\snot$|^not$|^can\s|\scan\s|\scan$|^can$|^all\s|\sall\s|\sall$|^all$|^one\s|\sone\s|\sone$|^one$|^any\s|\sany\s|\sany$|^any$|^have\s|\shave\s|\shave$|^have$|^that\s|\sthat\s|\sthat$|^that$|^with\s|\swith\s|\swith$|^with$|^this\s|\sthis\s|\sthis$|^this$|^they\s|\sthey\s|\sthey$|^they$|^from\s|\sfrom\s|\sfrom$|^from$|^what\s|\swhat\s|\swhat$|^what$|^will\s|\swill\s|\swill$|^will$|^them\s|\sthem\s|\sthem$|^them$|^would\s|\swould\s|\swould$|^would$|^about\s|\sabout\s|\sabout$|^about$|^there\s|\sthere\s|\sthere$|^there$|^which\s|\swhich\s|\swhich$|^which$|^could\s|\scould\s|\scould$|^could$|^an\s|\san\s|\san$|^an$|^are\s|\sare\s|\sare$|^are$|^is\s|\sis\s|\sis$|^is$|^was\s|\swas\s|\swas$|^was$|^ещё\s|\sещё\s|\sещё$|^ещё$|^ему\s|\sему\s|\sему$|^ему$|^которою\s|\sкоторою\s|\sкоторою$|^которою$|^всё\s|\sвсё\s|\sвсё$|^всё$|^той\s|\sтой\s|\sтой$|^той$|^ним\s|\sним\s|\sним$|^ним$|^мое\s|\sмое\s|\sмое$|^мое$|^вся\s|\sвся\s|\sвся$|^вся$|^эта\s|\sэта\s|\sэта$|^эта$|^нем\s|\sнем\s|\sнем$|^нем$|^моё\s|\sмоё\s|\sмоё$|^моё$|^нём\s|\sнём\s|\sнём$|^нём$|^моя\s|\sмоя\s|\sмоя$|^моя$|^нашею\s|\sнашею\s|\sнашею$|^нашею$|^всю\s|\sвсю\s|\sвсю$|^всю$|^эту\s|\sэту\s|\sэту$|^эту$|^одною\s|\sодною\s|\sодною$|^одною$|^нее\s|\sнее\s|\sнее$|^нее$|^неё\s|\sнеё\s|\sнеё$|^неё$|^ими\s|\sими\s|\sими$|^ими$)'
	query = re.sub(pattern,' ',query)
	query = ' '.join(query.split())
	return query