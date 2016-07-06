import collections
import pprint

with open('param/addresses_newkeywords.txt', 'r') as f:
	coords = []
	for line in f:
		citycoord = tuple(line.split(',')[:2])
		coords.append(citycoord)

	counter = collections.Counter(coords)

	#pprint.pprint(counter)
	pprint.pprint({('-23.5505199', '-46.6333094'): 20, ('-34.6036844', '-58.3815591'): 18, ('-19.9166813', '-43.9344931'): 11, ('-25.5165725', '-48.5229975'): 9, ('-23.442503', '-58.443832'): 8, ('-15.7942287', '-47.8821658'): 7, ('-22.9068467', '-43.1728965'): 7, ('-30.0346471', '-51.2176584'): 6, ('6.42375', '-66.58973'): 6, ('-14.235004', '-51.92528'): 6, ('-22.9139476', '-43.2093973'): 6, ('-25.2637399', '-57.575926'): 6, ('10.4805937', '-66.9036063'): 5, ('-38.416097', '-63.616672'): 5, ('4.7109886', '-74.072092'): 5, ('7.9137001', '-72.1416132'): 4, ('-18.512178', '-44.5550308'): 4, ('-3.1190275', '-60.0217314'): 4, ('40.463667', '-3.74922'): 4, ('40.7127837', '-74.0059413'): 3, ('-32.522779', '-55.765835'): 3, ('-21.7624237', '-43.3433999'): 3, ('4.570868', '-74.297333'): 3, ('-19.1834229', '-40.3088626'): 3, ('-19.7896207', '-42.1415419'): 3, ('23.634501', '-102.552784'): 3, ('-22.8968359', '-43.2787635'): 3, ('-26.9930938', '-48.6356285'): 3, ('-23.9678823', '-46.3288865'): 3, ('-25.2520888', '-52.0215415'): 2, ('-27.3621374', '-55.9008746'): 2, ('-20.1451261', '-44.8916447'): 2, ('-22.223561', '-54.8125486'): 2, ('-8.0578381', '-34.8828969'): 2, ('-20.4438418', '-44.7653198'): 2, ('-22.7862985', '-43.3053106'): 2, ('-22.7907664', '-43.3699364'): 2, ('18.4860575', '-69.9312117'): 2, ('43.212545', '-0.843547'): 2, ('34.0194543', '-118.4911912'): 2, ('-25.4289541', '-49.267137'): 2, ('-23.4314577', '-47.4625239'): 2, ('38.440429', '-122.7140548'): 2, ('19.2464696', '-99.1013498'): 2, ('-3.7318616', '-38.5266704'): 2, ('-22.9681736', '-43.3907025'): 2, ('33.6996066', '-117.7607569'): 2, ('26.4279706', '80.2962385'): 2, ('3.4516467', '-76.5319854'): 2, ('-31.6622189', '-60.7616339'): 2, ('-7.7955798', '110.3694896'): 2, ('-22.314459', '-49.0586951'): 2, ('-33.227158', '-60.3298704'): 2, ('-30.0346316', '-51.2176986'): 2, ('36.125278', '-90.924721'): 2, ('-23.589095', '-48.0487846'): 2, ('-29.3344108', '-49.723909'): 2, ('-12.9730401', '-38.502304'): 2, ('-20.1215224', '-40.3077898'): 2, ('-27.4269255', '-55.9467076'): 2, ('-20.2976178', '-40.2957768'): 2, ('-21.145344', '-41.6826186'): 2, ('13.6682174', '100.614025'): 2, ('28.6139391', '77.2090212'): 2, ('-21.2915055', '-50.3436312'): 2, ('53.46166', '-2.271707'): 2, ('-1.4557549', '-48.4901799'): 2, ('41.3850639', '2.1734035'): 2, ('56.879635', '24.603189'): 2, ('2.8235098', '-60.6758331'): 2, ('10.2011111', '-67.8990269'): 2, ('-23.6742228', '-46.5436003'): 2, ('-22.5125181', '-52.8694475'): 2, ('-20.7548659', '-42.8785788'): 2, ('-16.5045303', '-68.1211637'): 1, ('37.8656539', '-4.7787764'): 1, ('40.5004766', '141.5053076'): 1, ('50.9097004', '-1.4043509'): 1, ('11.8240433', '124.8403408'): 1, ('34.1477849', '-118.1445155'): 1, ('-27.2575078', '-55.5354048'): 1, ('35.2270869', '-80.8431267'): 1, ('-29.6690808', '-52.7882795'): 1, ('31.9685988', '-99.9018131'): 1, ('-23.5015299', '-47.4525603'): 1, ('-21.7844277', '-46.5780661'): 1, ('-22.7378463', '-47.3335688'): 1, ('-34.6558611', '-58.6167212'): 1, ('10.6095694', '-71.6327596'): 1, ('-22.8272883', '-43.0637646'): 1, ('41.4469883', '2.2450325'): 1, ('14.4728389', '121.0053777'): 1, ('-27.4257175', '-59.0243784'): 1, ('41.0616098', '-3.5064105'): 1, ('55.1028668', '67.0725632'): 1, ('12.879721', '121.774017'): 1, ('-16.6868912', '-49.2647943'): 1, ('48.6901541', '10.9208893'): 1, ('4.706035', '-74.230101'): 1, ('28.5383355', '-81.3792365'): 1, ('-28.2866506', '-53.4989324'): 1, ('17.7250472', '79.1546769'): 1, ('-35.675147', '-71.542969'): 1, ('40.2007986', '-7.6394055'): 1, ('-34.4979812', '-56.0389343'): 1, ('-29.991901', '-51.0813677'): 1, ('41.1844362', '-8.6962775'): 1, ('18.220833', '-66.590149'): 1, ('14.6760413', '121.0437003'): 1, ('-23.0972163', '-47.7144578'): 1, ('38.0405837', '-84.5037164'): 1, ('-29.1667089', '-51.5169861'): 1, ('33.4483771', '-112.0740373'): 1, ('33.7476649', '-84.3798319'): 1, ('-34.9204948', '-57.9535657'): 1, ('34.5199402', '-105.8700901'): 1, ('57.5384659', '25.4263618'): 1, ('-34.6019655', '-58.7771644'): 1, ('32.5423808', '-117.0254815'): 1, ('-0.1806532', '-78.4678382'): 1, ('-22.7561319', '-43.4607419'): 1, ('-7.790504', '-35.08157'): 1, ('-19.7473668', '-47.939154'): 1, ('-34.762001', '-58.2112961'): 1, ('-31.6476686', '-63.3444408'): 1, ('-0.3122566', '-78.5418531'): 1, ('9.7333906', '-63.1914317'): 1, ('20.9144491', '-100.745235'): 1, ('8.25205', '-73.3532199'): 1, ('-34.3643905', '-55.2590707'): 1, ('37.8043637', '-122.2711137'): 1, ('-21.2028539', '-50.4536793'): 1, ('-33.5139265', '-70.6930841'): 1, ('24.3943695', '54.5192066'): 1, ('-23.7699594', '-46.7004984'): 1, ('-21.5560669', '-45.4368543'): 1, ('-14.5462798', '-52.7941088'): 1, ('-21.7676522', '-43.3664041'): 1, ('-34.6610756', '-58.3669739'): 1, ('-8.8137173', '-36.954107'): 1, ('19.4325626', '-99.1850299'): 1, ('-7.934422', '-34.8687212'): 1, ('-22.7338724', '-45.1201112'): 1, ('-34.6994171', '-58.3926315'): 1, ('-21.1704008', '-47.8103238'): 1, ('-22.9099384', '-47.0626332'): 1, ('38.9071923', '-77.0368707'): 1, ('35.9940329', '-78.898619'): 1, ('-23.6113936', '-46.5289661'): 1, ('-16.6842776', '-44.364854'): 1, ('40.4116381', '-3.6602128'): 1, ('-33.2031488', '-70.6825268'): 1, ('-22.4169605', '-42.9756016'): 1, ('-31.3913921', '-58.017434'): 1, ('-22.8617133', '-47.1770446'): 1, ('4.9030522', '114.939821'): 1, ('39.1426987', '-84.8857679'): 1, ('-32.4644305', '-58.475069'): 1, ('43.2804038', '24.8643109'): 1, ('2.8038283', '101.4950699'): 1, ('-34.5281205', '-58.473816'): 1, ('39.0804218', '-94.4787733'): 1, ('-31.3301424', '-54.1004622'): 1, ('-22.87', '-43.3258333'): 1, ('-27.3245762', '-61.2813451'): 1, ('-22.573256', '-44.9693894'): 1, ('-15.5404411', '-47.3374297'): 1, ('29.4835264', '-95.6113704'): 1, ('48.856614', '2.3522219'): 1, ('-6.2595674', '-39.9260755'): 1, ('-22.2131635', '-49.6555394'): 1, ('-34.9079132', '-54.8255149'): 1, ('-2.2096412', '-79.8906045'): 1, ('-23.763171', '-45.9310409'): 1, ('-1.5039143', '40.0274159'): 1, ('-21.8901238', '-49.0314198'): 1, ('-0.3030988', '36.080026'): 1, ('11.4066536', '-69.6778973'): 1, ('6.2530408', '-75.5645737'): 1, ('-12.046374', '-77.0427934'): 1, ('14.5995124', '120.9842195'): 1, ('48.8555673', '15.285125'): 1, ('-29.6873064', '-53.8154769'): 1, ('43.653226', '-79.3831843'): 1, ('-9.6498487', '-35.7089492'): 1, ('-24.0436553', '-52.3781098'): 1, ('-23.3044524', '-51.1695824'): 1, ('46.572684', '12.536871'): 1, ('-26.1857768', '-58.1755669'): 1, ('13.6217753', '123.1948238'): 1, ('10.4953492', '-66.8759459'): 1, ('-31.4200833', '-64.1887761'): 1, ('-23.5328814', '-46.7920029'): 1, ('37.3639472', '-121.9289375'): 1, ('40.453868', '-105.0629797'): 1, ('-23.9948444', '-46.2568678'): 1, ('52.3702157', '4.8951679'): 1, ('45.764043', '4.835659'): 1, ('52.3905689', '13.0644729'): 1, ('46.2724015', '9.1695593'): 1, ('-20.811761', '-49.3762272'): 1, ('-23.733872', '-46.5759436'): 1, ('22.536712', '113.9781559'): 1, ('20.593684', '78.96288'): 1, ('-31.4679335', '-57.1013188'): 1, ('-10.7988901', '-66.9988011'): 1, ('-32.9442426', '-60.6505388'): 1, ('37.6658757', '-91.8479332'): 1, ('33.3806716', '-84.7996573'): 1, ('19.4713181', '-71.3395801'): 1, ('0.3697668', '-78.1210327'): 1, ('-33.881901', '25.59829'): 1, ('8.7489309', '-66.2367172'): 1, ('-22.5077674', '-44.0946129'): 1, ('1.352083', '103.819836'): 1, ('-23.4768588', '-46.8662018'): 1, ('-32.4665434', '-58.4787669'): 1, ('-22.9083081', '-43.1970258'): 1, ('6.6437076', '-73.6536209'): 1, ('-7.1194958', '-34.8450118'): 1, ('29.8399933', '77.1154368'): 1, ('-21.4261129', '-45.9481612'): 1, ('-22.8822363', '-43.3245974'): 1, ('52.0907374', '5.1214201'): 1, ('50.1649996', '14.680057'): 1, ('23.2610922', '-106.464468'): 1, ('3.5379718', '-76.2971657'): 1, ('-12.6971776', '-38.3331983'): 1, ('33.7489954', '-84.3879824'): 1, ('19.0759837', '72.8776559'): 1, ('8.5698244', '-71.1804988'): 1, ('18.5204303', '73.8567437'): 1, ('-7.70989', '29.776951'): 1, ('-30.559482', '22.937506'): 1, ('-24.0088727', '-46.4125034'): 1, ('32.459284', '85.93762'): 1, ('-24.1617068', '-54.0981117'): 1, ('25.7616798', '-80.1917902'): 1, ('28.2143574', '-82.7350514'): 1, ('-25.5163356', '-54.5853764'): 1, ('37.7749295', '-122.4194155'): 1, ('12.9548979', '77.6908171'): 1, ('37.9642529', '-91.8318334'): 1, ('-33.9248685', '18.4240553'): 1, ('-23.5431786', '-46.6291845'): 1, ('49.5479839', '6.3733466'): 1, ('46.9641127', '142.7347556'): 1, ('-26.8947924', '-48.6550692'): 1, ('-29.8885619', '-50.2698884'): 1, ('46.729553', '-94.6858998'): 1, ('37.331906', '-105.384531'): 1, ('14.5826355', '121.0134406'): 1, ('40.4167754', '-3.7037902'): 1, ('-17.7445191', '-48.6250248'): 1, ('42.708678', '19.37439'): 1, ('-2.5391099', '-44.2829046'): 1, ('35.907757', '127.766922'): 1, ('-37.4713077', '144.7851531'): 1, ('-27.6387496', '152.5928676'): 1, ('-20.0852508', '-59.4720904'): 1, ('-5.7864027', '-35.2079777'): 1, ('-27.0812841', '-53.1700599'): 1, ('53.9915028', '-1.5412015'): 1, ('38.2526647', '-85.7584557'): 1, ('-34.6045669', '-58.40145'): 1, ('-34.5291043', '-56.2873482'): 1, ('40.7607793', '-111.8910474'): 1, ('53.4807593', '-2.2426305'): 1, ('30.136493', '31.3298066'): 1, ('40.403923', '-73.9998987'): 1, ('-34.636595', '-58.364641'): 1, ('-35.6593239', '-63.7577887'): 1, ('-22.8858975', '-43.1152211'): 1, ('-19.9673078', '-44.2011904'): 1, ('51.481581', '-3.17909'): 1, ('46.061336', '14.508047'): 1, ('45.9570004', '10.3027318'): 1, ('-26.9165792', '-49.0717331'): 1, ('-23.6898429', '-46.5648481'): 1, ('23.9040878', '87.524748'): 1, ('4.210484', '101.975766'): 1, ('-34.425087', '-58.5796585'): 1, ('-20.6741197', '-40.4997382'): 1, ('10.2509303', '-66.4271499'): 1, ('-20.4269837', '-40.3280037'): 1, ('19.9858722', '73.7721234'): 1, ('34.0736204', '-118.4003563'): 1, ('-23.9607656', '-46.3960797'): 1, ('28.4594965', '77.0266383'): 1, ('50.0053767', '36.2314594'): 1, ('47.4922251', '-122.7639533'): 1, ('-34.7008742', '-58.479012'): 1, ('-34.6994795', '-58.3920795'): 1, ('-15.2475119', '-40.2509918'): 1, ('35.6894875', '139.6917064'): 1, ('-20.8483343', '-49.394625'): 1, ('26.1224386', '-80.1373174'): 1, ('33.6381378', '-117.5947168'): 1, ('-32.6610328', '-62.1161442'): 1, ('26.5118218', '-80.1570661'): 1, ('-27.3295727', '-58.9502013'): 1, ('29.7604267', '-95.3698028'): 1, ('55.0095761', '80.9631588'): 1, ('-22.9974848', '-44.303832'): 1, ('42.6891721', '23.3366764'): 1, ('-34.7611823', '-58.4302476'): 1, ('8.537981', '-80.782127'): 1, ('38.7131073', '-90.4298401'): 1, ('-15.826691', '-47.9218204'): 1})