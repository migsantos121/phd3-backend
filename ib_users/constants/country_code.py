__author__ = 'tanmay.ibhubs'

country_alpha_2 = {'Afghanistan': 'AF',
                   'Albania': 'AL',
                   'Algeria': 'DZ',
                   'American Samoa': 'AS',
                   'Andorra': 'AD',
                   'Angola': 'AO',
                   'Anguilla': 'AI',
                   'Antarctica': 'AQ',
                   'Antigua and Barbuda': 'AG',
                   'Argentina': 'AR',
                   'Armenia': 'AM',
                   'Aruba': 'AW',
                   'Australia': 'AU',
                   'Austria': 'AT',
                   'Azerbaijan': 'AZ',
                   'Bahamas': 'BS',
                   'Bahrain': 'BH',
                   'Bangladesh': 'BD',
                   'Barbados': 'BB',
                   'Belarus': 'BY',
                   'Belgium': 'BE',
                   'Belize': 'BZ',
                   'Benin': 'BJ',
                   'Bermuda': 'BM',
                   'Bhutan': 'BT',
                   'Bolivia, Plurinational State of': 'BO',
                   'Bonaire, Sint Eustatius and Saba': 'BQ',
                   'Bosnia and Herzegovina': 'BA',
                   'Botswana': 'BW',
                   'Bouvet Island': 'BV',
                   'Brazil': 'BR',
                   'British Indian Ocean Territory': 'IO',
                   'Brunei Darussalam': 'BN',
                   'Bulgaria': 'BG',
                   'Burkina Faso': 'BF',
                   'Burundi': 'BI',
                   "C\\u00f4te d'Ivoire": 'CI',
                   'Cabo Verde': 'CV',
                   'Cambodia': 'KH',
                   'Cameroon': 'CM',
                   'Canada': 'CA',
                   'Cayman Islands': 'KY',
                   'Central African Republic': 'CF',
                   'Chad': 'TD',
                   'Chile': 'CL',
                   'China': 'CN',
                   'Christmas Island': 'CX',
                   'Cocos (Keeling) Islands': 'CC',
                   'Colombia': 'CO',
                   'Comoros': 'KM',
                   'Congo': 'CG',
                   'Congo, The Democratic Republic of the': 'CD',
                   'Cook Islands': 'CK',
                   'Costa Rica': 'CR',
                   'Croatia': 'HR',
                   'Cuba': 'CU',
                   'Cura\\u00e7ao': 'CW',
                   'Cyprus': 'CY',
                   'Czechia': 'CZ',
                   'Denmark': 'DK',
                   'Djibouti': 'DJ',
                   'Dominica': 'DM',
                   'Dominican Republic': 'DO',
                   'Ecuador': 'EC',
                   'Egypt': 'EG',
                   'El Salvador': 'SV',
                   'Equatorial Guinea': 'GQ',
                   'Eritrea': 'ER',
                   'Estonia': 'EE',
                   'Ethiopia': 'ET',
                   'Falkland Islands (Malvinas)': 'FK',
                   'Faroe Islands': 'FO',
                   'Fiji': 'FJ',
                   'Finland': 'FI',
                   'France': 'FR',
                   'French Guiana': 'GF',
                   'French Polynesia': 'PF',
                   'French Southern Territories': 'TF',
                   'Gabon': 'GA',
                   'Gambia': 'GM',
                   'Georgia': 'GE',
                   'Germany': 'DE',
                   'Ghana': 'GH',
                   'Gibraltar': 'GI',
                   'Greece': 'GR',
                   'Greenland': 'GL',
                   'Grenada': 'GD',
                   'Guadeloupe': 'GP',
                   'Guam': 'GU',
                   'Guatemala': 'GT',
                   'Guernsey': 'GG',
                   'Guinea': 'GN',
                   'Guinea-Bissau': 'GW',
                   'Guyana': 'GY',
                   'Haiti': 'HT',
                   'Heard Island and McDonald Islands': 'HM',
                   'Holy See (Vatican City State)': 'VA',
                   'Honduras': 'HN',
                   'Hong Kong': 'HK',
                   'Hungary': 'HU',
                   'Iceland': 'IS',
                   'India': 'IN',
                   'Indonesia': 'ID',
                   'Iran, Islamic Republic of': 'IR',
                   'Iraq': 'IQ',
                   'Ireland': 'IE',
                   'Isle of Man': 'IM',
                   'Israel': 'IL',
                   'Italy': 'IT',
                   'Jamaica': 'JM',
                   'Japan': 'JP',
                   'Jersey': 'JE',
                   'Jordan': 'JO',
                   'Kazakhstan': 'KZ',
                   'Kenya': 'KE',
                   'Kiribati': 'KI',
                   "Korea, Democratic People's Republic of": 'KP',
                   'Korea, Republic of': 'KR',
                   'Kuwait': 'KW',
                   'Kyrgyzstan': 'KG',
                   "Lao People's Democratic Republic": 'LA',
                   'Latvia': 'LV',
                   'Lebanon': 'LB',
                   'Lesotho': 'LS',
                   'Liberia': 'LR',
                   'Libya': 'LY',
                   'Liechtenstein': 'LI',
                   'Lithuania': 'LT',
                   'Luxembourg': 'LU',
                   'Macao': 'MO',
                   'Macedonia, Republic of': 'MK',
                   'Madagascar': 'MG',
                   'Malawi': 'MW',
                   'Malaysia': 'MY',
                   'Maldives': 'MV',
                   'Mali': 'ML',
                   'Malta': 'MT',
                   'Marshall Islands': 'MH',
                   'Martinique': 'MQ',
                   'Mauritania': 'MR',
                   'Mauritius': 'MU',
                   'Mayotte': 'YT',
                   'Mexico': 'MX',
                   'Micronesia, Federated States of': 'FM',
                   'Moldova, Republic of': 'MD',
                   'Monaco': 'MC',
                   'Mongolia': 'MN',
                   'Montenegro': 'ME',
                   'Montserrat': 'MS',
                   'Morocco': 'MA',
                   'Mozambique': 'MZ',
                   'Myanmar': 'MM',
                   'Namibia': 'NA',
                   'Nauru': 'NR',
                   'Nepal': 'NP',
                   'Netherlands': 'NL',
                   'New Caledonia': 'NC',
                   'New Zealand': 'NZ',
                   'Nicaragua': 'NI',
                   'Niger': 'NE',
                   'Nigeria': 'NG',
                   'Niue': 'NU',
                   'Norfolk Island': 'NF',
                   'Northern Mariana Islands': 'MP',
                   'Norway': 'NO',
                   'Oman': 'OM',
                   'Pakistan': 'PK',
                   'Palau': 'PW',
                   'Palestine, State of': 'PS',
                   'Panama': 'PA',
                   'Papua New Guinea': 'PG',
                   'Paraguay': 'PY',
                   'Peru': 'PE',
                   'Philippines': 'PH',
                   'Pitcairn': 'PN',
                   'Poland': 'PL',
                   'Portugal': 'PT',
                   'Puerto Rico': 'PR',
                   'Qatar': 'QA',
                   'R\\u00e9union': 'RE',
                   'Romania': 'RO',
                   'Russian Federation': 'RU',
                   'Rwanda': 'RW',
                   'Saint Barth\\u00e9lemy': 'BL',
                   'Saint Helena, Ascension and Tristan da Cunha': 'SH',
                   'Saint Kitts and Nevis': 'KN',
                   'Saint Lucia': 'LC',
                   'Saint Martin (French part)': 'MF',
                   'Saint Pierre and Miquelon': 'PM',
                   'Saint Vincent and the Grenadines': 'VC',
                   'Samoa': 'WS',
                   'San Marino': 'SM',
                   'Sao Tome and Principe': 'ST',
                   'Saudi Arabia': 'SA',
                   'Senegal': 'SN',
                   'Serbia': 'RS',
                   'Seychelles': 'SC',
                   'Sierra Leone': 'SL',
                   'Singapore': 'SG',
                   'Sint Maarten (Dutch part)': 'SX',
                   'Slovakia': 'SK',
                   'Slovenia': 'SI',
                   'Solomon Islands': 'SB',
                   'Somalia': 'SO',
                   'South Africa': 'ZA',
                   'South Georgia and the South Sandwich Islands': 'GS',
                   'South Sudan': 'SS',
                   'Spain': 'ES',
                   'Sri Lanka': 'LK',
                   'Sudan': 'SD',
                   'Suriname': 'SR',
                   'Svalbard and Jan Mayen': 'SJ',
                   'Swaziland': 'SZ',
                   'Sweden': 'SE',
                   'Switzerland': 'CH',
                   'Syrian Arab Republic': 'SY',
                   'Taiwan, Province of China': 'TW',
                   'Tajikistan': 'TJ',
                   'Tanzania, United Republic of': 'TZ',
                   'Thailand': 'TH',
                   'Timor-Leste': 'TL',
                   'Togo': 'TG',
                   'Tokelau': 'TK',
                   'Tonga': 'TO',
                   'Trinidad and Tobago': 'TT',
                   'Tunisia': 'TN',
                   'Turkey': 'TR',
                   'Turkmenistan': 'TM',
                   'Turks and Caicos Islands': 'TC',
                   'Tuvalu': 'TV',
                   'Uganda': 'UG',
                   'Ukraine': 'UA',
                   'United Arab Emirates': 'AE',
                   'United Kingdom': 'GB',
                   'United States': 'US',
                   'United States Minor Outlying Islands': 'UM',
                   'Uruguay': 'UY',
                   'Uzbekistan': 'UZ',
                   'Vanuatu': 'VU',
                   'Venezuela, Bolivarian Republic of': 'VE',
                   'Viet Nam': 'VN',
                   'Virgin Islands, British': 'VG',
                   'Virgin Islands, U.S.': 'VI',
                   'Wallis and Futuna': 'WF',
                   'Western Sahara': 'EH',
                   'Yemen': 'YE',
                   'Zambia': 'ZM',
                   'Zimbabwe': 'ZW',
                   'Islands': 'AX'}

country_calling_code = {'Afghanistan': '+93',
                        'Albania': '+355',
                        'Algeria': '+213',
                        'American Samoa': '+1',
                        'Andorra': '+376',
                        'Angola': '+244',
                        'Anguilla': '+1',
                        'Antarctica': '+None',
                        'Antigua and Barbuda': '+1',
                        'Argentina': '+54',
                        'Armenia': '+374',
                        'Aruba': '+297',
                        'Australia': '+61',
                        'Austria': '+43',
                        'Azerbaijan': '+994',
                        'Bahamas': '+1',
                        'Bahrain': '+973',
                        'Bangladesh': '+880',
                        'Barbados': '+1',
                        'Belarus': '+375',
                        'Belgium': '+32',
                        'Belize': '+501',
                        'Benin': '+229',
                        'Bermuda': '+1',
                        'Bhutan': '+975',
                        'Bolivia, Plurinational State of': '+591',
                        'Bonaire, Sint Eustatius and Saba': '+599',
                        'Bosnia and Herzegovina': '+387',
                        'Botswana': '+267',
                        'Bouvet Island': '+None',
                        'Brazil': '+55',
                        'British Indian Ocean Territory': '+246',
                        'Brunei Darussalam': '+673',
                        'Bulgaria': '+359',
                        'Burkina Faso': '+226',
                        'Burundi': '+257',
                        'Cabo Verde': '+238',
                        'Cambodia': '+855',
                        'Cameroon': '+237',
                        'Canada': '+1',
                        'Cayman Islands': '+1',
                        'Central African Republic': '+236',
                        'Chad': '+235',
                        'Chile': '+56',
                        'China': '+86',
                        'Christmas Island': '+61',
                        'Cocos (Keeling) Islands': '+61',
                        'Colombia': '+57',
                        'Comoros': '+269',
                        'Congo': '+242',
                        'Congo, The Democratic Republic of the': '+243',
                        'Cook Islands': '+682',
                        'Costa Rica': '+506',
                        'Croatia': '+385',
                        'Cuba': '+53',
                        'Cyprus': '+357',
                        'Czechia': '+420',
                        'Denmark': '+45',
                        'Djibouti': '+253',
                        'Dominica': '+1',
                        'Dominican Republic': '+1',
                        'Ecuador': '+593',
                        'Egypt': '+20',
                        'El Salvador': '+503',
                        'Equatorial Guinea': '+240',
                        'Eritrea': '+291',
                        'Estonia': '+372',
                        'Ethiopia': '+251',
                        'Falkland Islands (Malvinas)': '+500',
                        'Faroe Islands': '+298',
                        'Fiji': '+679',
                        'Finland': '+358',
                        'France': '+33',
                        'French Guiana': '+594',
                        'French Polynesia': '+689',
                        'French Southern Territories': '+None',
                        'Gabon': '+241',
                        'Gambia': '+220',
                        'Georgia': '+995',
                        'Germany': '+49',
                        'Ghana': '+233',
                        'Gibraltar': '+350',
                        'Greece': '+30',
                        'Greenland': '+299',
                        'Grenada': '+1',
                        'Guadeloupe': '+590',
                        'Guam': '+1',
                        'Guatemala': '+502',
                        'Guernsey': '+44',
                        'Guinea': '+224',
                        'Guinea-Bissau': '+245',
                        'Guyana': '+592',
                        'Haiti': '+509',
                        'Heard Island and McDonald Islands': '+None',
                        'Holy See (Vatican City State)': '+39',
                        'Honduras': '+504',
                        'Hong Kong': '+852',
                        'Hungary': '+36',
                        'Iceland': '+354',
                        'India': '+91',
                        'Indonesia': '+62',
                        'Iran, Islamic Republic of': '+98',
                        'Iraq': '+964',
                        'Ireland': '+353',
                        'Isle of Man': '+44',
                        'Israel': '+972',
                        'Italy': '+39',
                        'Jamaica': '+1',
                        'Japan': '+81',
                        'Jersey': '+44',
                        'Jordan': '+962',
                        'Kazakhstan': '+7',
                        'Kenya': '+254',
                        'Kiribati': '+686',
                        "Korea, Democratic People's Republic of": '+850',
                        'Korea, Republic of': '+82',
                        'Kuwait': '+965',
                        'Kyrgyzstan': '+996',
                        "Lao People's Democratic Republic": '+856',
                        'Latvia': '+371',
                        'Lebanon': '+961',
                        'Lesotho': '+266',
                        'Liberia': '+231',
                        'Libya': '+218',
                        'Liechtenstein': '+423',
                        'Lithuania': '+370',
                        'Luxembourg': '+352',
                        'Macao': '+853',
                        'Macedonia, Republic of': '+389',
                        'Madagascar': '+261',
                        'Malawi': '+265',
                        'Malaysia': '+60',
                        'Maldives': '+960',
                        'Mali': '+223',
                        'Malta': '+356',
                        'Marshall Islands': '+692',
                        'Martinique': '+596',
                        'Mauritania': '+222',
                        'Mauritius': '+230',
                        'Mayotte': '+262',
                        'Mexico': '+52',
                        'Micronesia, Federated States of': '+691',
                        'Moldova, Republic of': '+373',
                        'Monaco': '+377',
                        'Mongolia': '+976',
                        'Montenegro': '+382',
                        'Montserrat': '+1',
                        'Morocco': '+212',
                        'Mozambique': '+258',
                        'Myanmar': '+95',
                        'Namibia': '+264',
                        'Nauru': '+674',
                        'Nepal': '+977',
                        'Netherlands': '+31',
                        'New Caledonia': '+687',
                        'New Zealand': '+64',
                        'Nicaragua': '+505',
                        'Niger': '+227',
                        'Nigeria': '+234',
                        'Niue': '+683',
                        'Norfolk Island': '+672',
                        'Northern Mariana Islands': '+1',
                        'Norway': '+47',
                        'Oman': '+968',
                        'Pakistan': '+92',
                        'Palau': '+680',
                        'Palestine, State of': '+970',
                        'Panama': '+507',
                        'Papua New Guinea': '+675',
                        'Paraguay': '+595',
                        'Peru': '+51',
                        'Philippines': '+63',
                        'Pitcairn': '+None',
                        'Poland': '+48',
                        'Portugal': '+351',
                        'Puerto Rico': '+1',
                        'Qatar': '+974',
                        'Romania': '+40',
                        'Russian Federation': '+7',
                        'Rwanda': '+250',
                        'Saint Helena, Ascension and Tristan da Cunha': '+290',
                        'Saint Kitts and Nevis': '+1',
                        'Saint Lucia': '+1',
                        'Saint Martin (French part)': '+590',
                        'Saint Pierre and Miquelon': '+508',
                        'Saint Vincent and the Grenadines': '+1',
                        'Samoa': '+685',
                        'San Marino': '+378',
                        'Sao Tome and Principe': '+239',
                        'Saudi Arabia': '+966',
                        'Senegal': '+221',
                        'Serbia': '+381',
                        'Seychelles': '+248',
                        'Sierra Leone': '+232',
                        'Singapore': '+65',
                        'Sint Maarten (Dutch part)': '+1',
                        'Slovakia': '+421',
                        'Slovenia': '+386',
                        'Solomon Islands': '+677',
                        'Somalia': '+252',
                        'South Africa': '+27',
                        'South Georgia and the South Sandwich Islands': '+None',
                        'South Sudan': '+211',
                        'Spain': '+34',
                        'Sri Lanka': '+94',
                        'Sudan': '+249',
                        'Suriname': '+597',
                        'Svalbard and Jan Mayen': '+47',
                        'Swaziland': '+268',
                        'Sweden': '+46',
                        'Switzerland': '+41',
                        'Syrian Arab Republic': '+963',
                        'Taiwan, Province of China': '+886',
                        'Tajikistan': '+992',
                        'Tanzania, United Republic of': '+255',
                        'Thailand': '+66',
                        'Timor-Leste': '+670',
                        'Togo': '+228',
                        'Tokelau': '+690',
                        'Tonga': '+676',
                        'Trinidad and Tobago': '+1',
                        'Tunisia': '+216',
                        'Turkey': '+90',
                        'Turkmenistan': '+993',
                        'Turks and Caicos Islands': '+1',
                        'Tuvalu': '+688',
                        'Uganda': '+256',
                        'Ukraine': '+380',
                        'United Arab Emirates': '+971',
                        'United Kingdom': '+44',
                        'United States': '+1',
                        'United States Minor Outlying Islands': '+None',
                        'Uruguay': '+598',
                        'Uzbekistan': '+998',
                        'Vanuatu': '+678',
                        'Venezuela, Bolivarian Republic of': '+58',
                        'Viet Nam': '+84',
                        'Virgin Islands, British': '+1',
                        'Virgin Islands, U.S.': '+1',
                        'Wallis and Futuna': '+681',
                        'Western Sahara': '+212',
                        'Yemen': '+967',
                        'Zambia': '+260',
                        'Zimbabwe': '+263',
                        'Islands': '+358'}

alpha_2_calling_code = {'AD': '+376',
                        'AE': '+971',
                        'AF': '+93',
                        'AG': '+1',
                        'AI': '+1',
                        'AL': '+355',
                        'AM': '+374',
                        'AO': '+244',
                        'AQ': '+None',
                        'AR': '+54',
                        'AS': '+1',
                        'AT': '+43',
                        'AU': '+61',
                        'AW': '+297',
                        'AX': '+358',
                        'AZ': '+994',
                        'BA': '+387',
                        'BB': '+1',
                        'BD': '+880',
                        'BE': '+32',
                        'BF': '+226',
                        'BG': '+359',
                        'BH': '+973',
                        'BI': '+257',
                        'BJ': '+229',
                        'BL': '+590',
                        'BM': '+1',
                        'BN': '+673',
                        'BO': '+591',
                        'BQ': '+599',
                        'BR': '+55',
                        'BS': '+1',
                        'BT': '+975',
                        'BV': '+None',
                        'BW': '+267',
                        'BY': '+375',
                        'BZ': '+501',
                        'CA': '+1',
                        'CC': '+61',
                        'CD': '+243',
                        'CF': '+236',
                        'CG': '+242',
                        'CH': '+41',
                        'CI': '+225',
                        'CK': '+682',
                        'CL': '+56',
                        'CM': '+237',
                        'CN': '+86',
                        'CO': '+57',
                        'CR': '+506',
                        'CU': '+53',
                        'CV': '+238',
                        'CW': '+599',
                        'CX': '+61',
                        'CY': '+357',
                        'CZ': '+420',
                        'DE': '+49',
                        'DJ': '+253',
                        'DK': '+45',
                        'DM': '+1',
                        'DO': '+1',
                        'DZ': '+213',
                        'EC': '+593',
                        'EE': '+372',
                        'EG': '+20',
                        'EH': '+212',
                        'ER': '+291',
                        'ES': '+34',
                        'ET': '+251',
                        'FI': '+358',
                        'FJ': '+679',
                        'FK': '+500',
                        'FM': '+691',
                        'FO': '+298',
                        'FR': '+33',
                        'GA': '+241',
                        'GB': '+44',
                        'GD': '+1',
                        'GE': '+995',
                        'GF': '+594',
                        'GG': '+44',
                        'GH': '+233',
                        'GI': '+350',
                        'GL': '+299',
                        'GM': '+220',
                        'GN': '+224',
                        'GP': '+590',
                        'GQ': '+240',
                        'GR': '+30',
                        'GS': '+None',
                        'GT': '+502',
                        'GU': '+1',
                        'GW': '+245',
                        'GY': '+592',
                        'HK': '+852',
                        'HM': '+None',
                        'HN': '+504',
                        'HR': '+385',
                        'HT': '+509',
                        'HU': '+36',
                        'ID': '+62',
                        'IE': '+353',
                        'IL': '+972',
                        'IM': '+44',
                        'IN': '+91',
                        'IO': '+246',
                        'IQ': '+964',
                        'IR': '+98',
                        'IS': '+354',
                        'IT': '+39',
                        'JE': '+44',
                        'JM': '+1',
                        'JO': '+962',
                        'JP': '+81',
                        'KE': '+254',
                        'KG': '+996',
                        'KH': '+855',
                        'KI': '+686',
                        'KM': '+269',
                        'KN': '+1',
                        'KP': '+850',
                        'KR': '+82',
                        'KW': '+965',
                        'KY': '+1',
                        'KZ': '+7',
                        'LA': '+856',
                        'LB': '+961',
                        'LC': '+1',
                        'LI': '+423',
                        'LK': '+94',
                        'LR': '+231',
                        'LS': '+266',
                        'LT': '+370',
                        'LU': '+352',
                        'LV': '+371',
                        'LY': '+218',
                        'MA': '+212',
                        'MC': '+377',
                        'MD': '+373',
                        'ME': '+382',
                        'MF': '+590',
                        'MG': '+261',
                        'MH': '+692',
                        'MK': '+389',
                        'ML': '+223',
                        'MM': '+95',
                        'MN': '+976',
                        'MO': '+853',
                        'MP': '+1',
                        'MQ': '+596',
                        'MR': '+222',
                        'MS': '+1',
                        'MT': '+356',
                        'MU': '+230',
                        'MV': '+960',
                        'MW': '+265',
                        'MX': '+52',
                        'MY': '+60',
                        'MZ': '+258',
                        'NA': '+264',
                        'NC': '+687',
                        'NE': '+227',
                        'NF': '+672',
                        'NG': '+234',
                        'NI': '+505',
                        'NL': '+31',
                        'NO': '+47',
                        'NP': '+977',
                        'NR': '+674',
                        'NU': '+683',
                        'NZ': '+64',
                        'OM': '+968',
                        'PA': '+507',
                        'PE': '+51',
                        'PF': '+689',
                        'PG': '+675',
                        'PH': '+63',
                        'PK': '+92',
                        'PL': '+48',
                        'PM': '+508',
                        'PN': '+None',
                        'PR': '+1',
                        'PS': '+970',
                        'PT': '+351',
                        'PW': '+680',
                        'PY': '+595',
                        'QA': '+974',
                        'RE': '+262',
                        'RO': '+40',
                        'RS': '+381',
                        'RU': '+7',
                        'RW': '+250',
                        'SA': '+966',
                        'SB': '+677',
                        'SC': '+248',
                        'SD': '+249',
                        'SE': '+46',
                        'SG': '+65',
                        'SH': '+290',
                        'SI': '+386',
                        'SJ': '+47',
                        'SK': '+421',
                        'SL': '+232',
                        'SM': '+378',
                        'SN': '+221',
                        'SO': '+252',
                        'SR': '+597',
                        'SS': '+211',
                        'ST': '+239',
                        'SV': '+503',
                        'SX': '+1',
                        'SY': '+963',
                        'SZ': '+268',
                        'TC': '+1',
                        'TD': '+235',
                        'TF': '+None',
                        'TG': '+228',
                        'TH': '+66',
                        'TJ': '+992',
                        'TK': '+690',
                        'TL': '+670',
                        'TM': '+993',
                        'TN': '+216',
                        'TO': '+676',
                        'TR': '+90',
                        'TT': '+1',
                        'TV': '+688',
                        'TW': '+886',
                        'TZ': '+255',
                        'UA': '+380',
                        'UG': '+256',
                        'UM': '+None',
                        'US': '+1',
                        'UY': '+598',
                        'UZ': '+998',
                        'VA': '+39',
                        'VC': '+1',
                        'VE': '+58',
                        'VG': '+1',
                        'VI': '+1',
                        'VN': '+84',
                        'VU': '+678',
                        'WF': '+681',
                        'WS': '+685',
                        'YE': '+967',
                        'YT': '+262',
                        'ZA': '+27',
                        'ZM': '+260',
                        'ZW': '+263'}
