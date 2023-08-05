#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
alphabet = list(map(chr, range(97, 123)))

roman = "aath,aauda,aaye,abadda,abastha,abela,abhilasa,abhilasha,abhiyan,abhyas,accident,account,accountant,acharya,activity,adachya,adaksha,adhaksha,adhyan,adhyaya,afnai,afni,afno,after,aimai,airport,ajabholi,ajakal,akash,akhabara,akhir ,akraman,alchi,alu,ama,amar,ambika,america,amilo,amrika,amrit,anamika,andolan,angur,animal,ankha,antarbarta,antarvarta,anuhar,anusandhan,anusar,anyatha,approve,april,apthero,arabia,argentina,arghakhachi,arghakhanchi,army,arsenal,artha,article,arun,arunima,asadhya,asar,asia,ason,associa,ashesh,sambidhan,banepali,banjade,balaji,baral,basnet,bisht,bhusal,belbase,chhetry,dahal,dangol,dhakal,chaudhary,chapagai,chapagain,chaulagai,chaulagain,dawadi,devkota,hamal,jha,jimba,khan,kafle,karki,lamichhane,mainali,manandhar,obama,patel,rijal,sapkota,siwakoti,shakya,sherpa,silwal,tamang,tuladhar,yadav,adil,amit,abishek,aman,amitabh,amogh,baba,balram,baliram,bhagat,bhagwan,bhaskar,bhawani,bidhan,bidyut,bijay,binayak,chirag,falgunanda,chiring,chhiring,gandhi,gokarna,imran,kaji,kedar,kranti,kunal,lakpa,lalit,laxman,loknath,murari,mrp,nagendra,nanak,nishant,palash,paras,prashant,prabhakar,prachanda,prahalad,pratap,raghav,rahul,raj,rajeev,rajiv,rajkumar,rajkumari,rakesh,ricky,rishi,ronaldo,sajid,sarthak,saunak,salman,siddhartha,sunny,suraj,shyam,tushar,udit,yash,yubraj,yuvraj,alina,alisha,amrita,anisha,anupama,basanti,bipasha,dhankumari,deepa,deepali,dikshya,janaki,jayanta,ganga,geeta,kaili,kareena,karisma,karishma,kumari,maili,maiya,mankumari,madhurima,naina,naveena,nisha,nanu,parijat,payal,pooja,priyanka,prabha,pragya,prerna,prerana,prajwala,pratikshya,rampyari,radhika,rakshya,rina,rekha,ruby,samjhana,sangita,sangeeta,saili,sharada,shova,supriya,uma,usha,bardiya,bhim datta,birganj,birtamod,birendranagar,chapagaun,champapur,chautara,danfe,darchula,dhapasi,dipayal,dhanusadham,dhanushadham,dolakha,fulchoki,fulchowki,gulariya,gadhimai,gaushala,godawari,gosaikunda,hanumandhoka,kakani,kalaiya,kamalamai,kantipath,karyabinayak,khaptad,khokana,kohalpur,mirchaiya,namche,parsa,panchkhal,phulchoki,phulchowki,mangalbazar,muktinath,nepalganj,nijgadh,rara,tulsipur,tikapur,shankarapur,siddharthanagar,swargadwari,urlabari,dulegaunda,aeko,agraha,aijo,aja,and,arthik,ayo,akha,aparadh,aparadhi,bagh,battery,baithak,balak,balika,banijya,bewasta,bhatbhateni,bheda,bhuichalo,bhukampa,bibad,bigyapan,billa,biralo,black,blood,bhanda,byaktigat,calendar,celebrity,chalak,chara,chhalfal,chhadera,chhata,chhath,chhito,confirm,crore,dastabej,damkal,deal,dekhau,deusi,devdas,dhara,dipawali,dhalan,dv,dristikon,drishtikon,fanta,fire,gadi,gaida,google,grihapristha,hajar,happy,hati,hunata,iphone,international,janani,janawar,jamma,janma,jam,karod,kathin,kamaune,kanun,kanuni,khalko,khali,khanaa,khane,lakh,laddu,laptop,matabhed,mataved,memory,maulikta,mithai,motorola,miss,mahakabi,mamaghar,naya,nepalese,new,nasha,nari,nirdeshan,nokia,nidra,nindra,nata,national,nurse,nyaya,online,otel,paisa,papa,pakistan,paunu,peda,photo,pran,prawas,rojgar,sampadakiya,sankat,sirsa,shirsa,square,samparka,smart,sadarmukam,samma,samsung,sanstha,side,sitamol,star,super,sujay,swasthya,taja,tanker,tayari,technology,thado,ticket,thakur,trend,wanted,wala,ulto,upadhi,white,vana,vane,villain,yar,yahoo,year,astha,aswin,atanka,atankakari,athawa,audai,audio,august,aula,auna,aunty,ausadhi,australia,avastha,avyas,awastha,ayojana,babu,back,badamas,badhai,badhi,badmas,badri,baglung,bagmati,bahadur,baikuntha,baisakh,baitadi,bajar,bajhang,bajura,bakhra,balaju,banepa,baneswar,baneswore,bangkok,bangladesh,bank,banke,bansbari,bara,baralida,baralina,bardia,bare,bari,barsa,barsha,barsik,basbari,bastab,bastav,bata,batabaran,batau,bath,bato,bazar,bazi,bbc,beer,belgium,bhadgaon,bhadrakali,bhag,bhana"
roman_list = roman.split(',')
nepali ="आठ,आउँदा,आए,आबद्द,अवस्था,अबेला,अभिलाषा,अभिलाषा,अभियान,अभ्यास,एक्सिडेन्ट्,अकाउन्ट्,अकाउन्टेन्ट,आचार्य,एक्टिभिटी,अध्यक्ष,अध्यक्ष,अध्यक्ष,अध्ययन,अध्याय,आफ्नै,आफ्नी,आफ्नो,आफ्टर,आईमाई,एअरपोर्ट,आजभोलि,आजकाल,आकाश,अखबार,अखिर ,आक्रमण,अल्छि,आलु,आमा,अमर,अम्बिका,अमेरिका,अमिलो,अम्रिका,अमृत,अनामिका,आन्दोलन,अङ्गुर,यानिमल,आँखा,अन्तर्वाता,अन्तर्वाता,अनुहार,अनुसन्धान,अनुसार,अन्यथा,अप्रुभ,अप्रिल,अप्ठेरो,अरेबिया,अर्जेन्टिना,अर्घाखाँची,अर्घाखाँची,आर्मी,आर्सनल,अर्थ,आर्टिकल,अरुण,अरुणिमा,असाध्य,असार,एसिया,असन,एसोसिए,अशेष,संविधानन,बनेपाली,बन्जाडे,बालाजी,बराल,बस्नेत,बिष्ट,भुसाल,बेल्बासे,छेत्री,दाहाल,डंगोल,धकाल,चौधरी,चापागाई,चापागाई,चौलागाई,चौलागाई,डवाडी,देवकोटा,हमाल,झा,जिम्बा,खान,काफ्ले,कार्की,लामिछाने,मैनाली,मानन्धर,ओबामा,पटेल,रिजाल,सापकोटा,शिवाकोटी,शाक्य,शेर्पा,सिल्वाल,तामाङ,तुलाधर,यादव,आदिल,अमित,अभिसेक,अमन,अमिताभ,अमोघ,बाबा,बलराम,बलिराम,भगत,भग्वान,भास्कर,भवानी,बिधान,विद्यूत,बिजय,बिनायक,बिनायक,फाल्गुनन्द,छिरिङ्,छिरिङ्,गान्धी,गोकर्ण,इमरान,काजी,केदार,क्रान्ती,कुनाल,लाक्पा,केदार,लक्ष्मण,लोकनाथ,मुरारी,एमआरपी,केदार,नानक,निशान्त,पलाश,पारस,प्रशान्त,प्रभाकर,प्रचन्ड,प्रहलाद,प्रताप,राघव,राहुल,राज,राजीव,राजीव,राजकुमार,राजकुमारी,राकेश,रिक्की,ऋषि,रोनाल्डो,साजीद,सार्थक,सौनक,सल्मान,सिद्धार्थ,सन्नी,सुरज,श्याम,तुशार,उदीत,यश,युवराज,युवराज,एलिना,अलिशा,अमृता,अनिशा,अनुपमा,बसन्ती,बिपाशा,धनकुमारी,दीपा,दीपाली,दीक्षा,जानकी,जयन्ता,गङ्गा,गीता,काईली,करीना,करिश्मा,करिश्मा,कुमारी,माईली,मैया,मनकुमारी,मधुरिमा,नैना,नवीना,निशा,नानु,परिजात,पायल,पूजा,प्रियंका,प्रभा,प्रज्ञा,प्रेरणा,प्रेरणा,प्रज्वला,प्रतिक्षा,रामप्यारी,राधिका,रक्षा,रीना,रेखा,रुबी,समझना,संगीता,संगीता,साईली,शारदा,शोभा,सुप्रिया,उमा,उशा,बर्दिया,भिम दत्त,बिरगंज,बिर्तामोड,बिरेन्द्रनगर,चापागाउँ,चम्पापुर,चौतारा,डाँफे,दर्चुला,धापासी,दिपायल,धनुषाधाम,धनुषाधाम,दोलखा,फूल्चोकी,फूल्चोकी,गुलरीया,गढीमाई,गौशाला,गोदावरी,गोसाईकुन्ड,हनुमानढोका,ककनी,कलईया,कमलामाई,कान्तिपथ,कार्यबिनायक,खप्तड,खोकना,कोहलपुर,मिर्चैया,नाम्चे,पर्सा,पाँचखाल,फूल्चोकी,फूल्चोकी,मङ्गलबजार,मुक्तिनाथ,नेपालगन्ज,निजगढ,रारा,तुल्सीपुर,तिकापुर,शंकरापुर,सिद्धार्थनगर,स्वर्गद्वारी,उर्लाबारी,दुलेगौंडा,अएको,आग्रह,आइजो,आज,एन्ड,आर्थिक,आयो,आँखा,अपराध,अपराधी,बाघ,ब्याट्री,बैठक,बालक,बालिका,वाणिज्य,वेवास्ता,भाट्भटेनि,भेडा,भुइँचालो,भूकम्प,विवाद,विज्ञापन,बिल्ला,बिरालो,ब्ल्याक्,ब्लड,भन्दा,व्यक्तिगत,क्यालेन्डर,सेलिब्रेटी,चालक,चरा,छलफल,छाडेर,छाता,छठ,छिटो,कन्फर्म,करोड,दस्ताबेज,दमकल,डिल,देखाउ,देउसी,देवदास,धारा,दीपावली,ढलान,डिभी,दृष्टीकोण,दृष्टीकोण,फ्यानटा,फाएर,गाडी,गैंडा,गूगल,गृहपृष्ठ,हजार,ह्याप्पी,हाती,हुनत,आईफोन,ईन्टरनेशनल,जननी,जनावर,जम्मा,जन्म,जाम,करोड,कठिन,कमाउने,कानुन,कानुनी,खाल्को,खाली,खाने,खाने,लाख,लड्डु,ल्यापटप,मतभेद,मतभेद,मेमोरी,थाकुर,मिठाई,मोटोरोला,मिस,महाकवि,मामाघर,नयाँ,नेपलीज,न्यू,नशा,नारी,निर्देशन,नोकिया,निद्रा,निद्रा,नाता,न्याश्नल,नर्स,न्याय,अन्लाईन,ओटेल,पैसा,पापा,पाकिस्तान,पाउनु,पेडा,फोटो,प्राण,प्रवास,रोज्गार,सम्पादकीय,संकट,शीर्ष,शीर्ष,स्क्याएर,सम्पर्क,स्मार्ट,सदरमुकाम,सम्म,सामसुङ,संस्था,साईड,सिटामोल,स्टार,सुपर,सुजय,स्वास्थ्य,ताजा,ट्यांकर,तयारी,टेक्नोलोजी,थाडो,टिकट,थाकुर,ट्रेन्ड,वान्टेड,वाला,उल्टो,उपाधि,वाईट,भन,भने,भिलेन,यार,याहू,न्यू,आस्था,आस्विन,आतंक,आतंककारी,अथवा,आउँदै,अडियो,अगस्त,औंला,आउन,आन्टी,औषधी,अष्ट्रेलिया,अवस्था,अभ्यास,अवस्था,आयोजना,बाबु,ब्याक,बदमाश,बधाई,बढी,बदमाश,बद्री,बाग्लुङ,बागमती,बहादुर,बैकुण्ठ,बैशाख,बैतडी,बजार,बझाङ,बाजुरा,बाख्रा,बालाजु,बनेपा,बानेश्वर,बानेश्वर,बैंकक,बाङ्लादेश,बैंक,बाँके,बाँसबारी,बारा,बरालिँदा,बरालिन,बर्दिया,बारे,बारी,बर्ष,बर्षा,वार्षिक,बाँसबारी,वास्तव,वास्तव,बाट,बातावरण,बताउ,बाथ,बाटो,बजार,बाजी,बिबिसी,बियर,बेल्जियम,भादगाउँ,भद्रकाली,भाग,भन"
nepali_list = nepali.split(',')

print(len(roman_list))
print(len(nepali_list))

online_dist = OrderedDict(zip(roman_list,nepali_list))

d2r_dict=OrderedDict([
	('dar','डर'), 
	('malai','मलाई'),
	('hamro','हम्रो'),
	('napala','नेपाल'),
	('napala','नेपाल'),
	('bharat','भारत'), 
	('bharat','इंडिया'), 
 	('surakshit','सुरक्षित'),
 	('suraksha','सुरक्षा'),
  	('suraksha','सुरक्षा'), 
	('thau','ठाउँ'),  
	('corona','कोरोना'),
	('aile','अहिले'),
	('aaile','अहिले'),
	('Covid19​','कोरोना'), 
	('SARS-CoV-2','कोरोना'), 
	('aama','आमा'), 
	('aamaa','आमा'), 
	('hoina','होइन'), 
	('koslai','कस्लाई'), 
	('khatarnak','खतरनाक'),
	('pariwartan','परिवर्तन'),  
	('kaslai','कस्लाई'), 
	('sambav','सम्भव'), 
	('virus','भाइरस'), 
	('vairus','भाइरस'), 
	('co','को'), 
	('bha','भ'), 
	('ca','च'), 
	('tim','तिम्'), 
	('ti','ति'), 
	('ta','त'), 
	('rai','राई'), 
	('cha','छ'),
	('chha','छ'),
	('xa','छ'),  
	('da','द'), 
	('dha','ध'),
	('gha','घ'),    
	('fa','फा'),
	('pha','फ'),
	('ga','ग'), 
	('ra','र'),   
	('qa','का'), 
	('sha','श'),              
	('sh','श'), 
	('ta','त'),
	('tha','ठ'),
	('aau','औ'),
	('sa','स'),
	('wa','वा'), 
	('ai','ई'), 
	('ya','या'), 
	('am','आम'), 
	('au','औ'), 
	('aum','ओम'),  
	('ja','ज'),
	('jha','झा'),
	('gya','ग्या'),
	('yan','यन'),
	('nga','ङ्ग'),
	('ma','म'),
	('za','श'),
	('ksha','क्ष'),
	('ksha','क्ष'),
	('la','ल'),
	('om','ओम'),
	('rri','रि'),
	('oo','ओ'),
	('na','न'),
	('ka','क'),
	('ja','ज'),
	('a','ा'), 
	('b','ब'), 
	('c','च'), 
	('d','द'), 
	('e','े'), 
	('f','उ'), 
	('g','ग'), 
	('h','ह'), 
	('i','ि'), 
	('j','ज'), 
	('k','क'), 
	('l','ल'), 
	('n','न'), 
	('m','म'), 
	('o','ो'),
	('pa','प'), 
	('p','प'), 
	('q','ट'), 
	('r','र'), 
	('s','स'), 
	('t','त'), 
	('u','ु'), 
	('v','व'), 
	('w','ौ'), 
	('x','ड'), 
	('y','य'), 
	('z','ष')
	])


online_dist.update(d2r_dict)
def is_devanagari(text):
	"""
	This function checks if the text is in Devanagari format.
	Syntax:
	>>> nt.is_devanagari(text)

	Example:
		>>> import nepali_transliteration as nt
		>>> nt.is_devanagari("कोरोना")
			True

		>>> nt.romanize_text("nepalकोरोना")
			False

		>>> nt.romanize_text("corona")
			False
	"""
	if(sum(True for i in text if i.lower() in set(alphabet)) / len(text)) > 0.0:
		return False
	else:
		return True
   

def convert(text):
	"""
	This function can be used to convert romanize text into nepali.

	Syntax:
	>>> nt.convert(text)

	Example:
		>>> import nepali_transliteration as nt
		>>> nt.convert("corona")
			कोरोना
	"""
	text = text.lower()
	for key,value in online_dist.items():
		text=text.replace(key,value)  
	return text

# def main():
#      print(convert("aath account rara desh nepal ho hi k ho timro naam"))


# if __name__== "__main__":
#   main()

