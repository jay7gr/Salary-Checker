# Retirement tool: Safety Index (0-100, Numbeo-style)
# Reference: Tokyo=74, Bangkok=62, Bali=60, Prague=70, Bogota=25
NEW_SAFETY = {
    'Faro': 72, 'Canggu': 55, 'Koh Samui': 60, 'Da Nang': 65, 'Hoi An': 68,
    'Hua Hin': 62, 'Puerto Vallarta': 48, 'Tulum': 45, 'Mazatlán': 42,
    'Cádiz': 70, 'Taormina': 72, 'Kotor': 74, 'Cascais': 78, 'Las Palmas': 68,
    'Santa Cruz de Tenerife': 70, 'Paphos': 78, 'Limassol': 75, 'Nha Trang': 62,
    'Siargao': 55, 'El Nido': 58, 'Essaouira': 58, 'Punta Cana': 50, 'Zanzibar': 48,
    'Cuenca': 55, 'Da Lat': 68, 'Ubud': 62, 'Innsbruck': 82, 'Interlaken': 85,
    'San Cristóbal de las Casas': 42, 'Oaxaca': 45, 'Antigua Guatemala': 42,
    'Pokhara': 55, 'Luang Prabang': 60,
    'Colombo': 52, 'Accra': 45, 'Tunis': 48, 'Tangier': 52, 'Amman': 62,
    'Beirut': 35, 'Muscat': 78, 'Batumi': 62, 'Yerevan': 65, 'Vientiane': 58,
    'Yangon': 42, 'Kampala': 38, 'Addis Ababa': 32, 'Dakar': 42, 'Kathmandu': 45,
    'Bratislava': 68, 'Ljubljana': 78, 'Vilnius': 72, 'Plovdiv': 70,
    'Sofia': 65, 'Belgrade': 58, 'Sarajevo': 62, 'Tirana': 52,
    'Funchal': 80, 'Palma de Mallorca': 72,
    'Mérida': 52, 'Quito': 38, 'La Paz': 35, 'Santo Domingo': 40,
    'San Juan': 42,
    'Chiang Rai': 68, 'Ipoh': 65, 'Dumaguete': 58, 'Jeju': 80,
    'Taichung': 78, 'Vung Tau': 62,
}

# Healthcare Index (0-100)
# Reference: Japan/Korea=88, Thailand=77, Indonesia=52, Eastern Europe=55-70
NEW_HEALTHCARE = {
    'Faro': 68, 'Canggu': 48, 'Koh Samui': 65, 'Da Nang': 55, 'Hoi An': 48,
    'Hua Hin': 62, 'Puerto Vallarta': 60, 'Tulum': 45, 'Mazatlán': 52,
    'Cádiz': 72, 'Taormina': 65, 'Kotor': 52, 'Cascais': 72, 'Las Palmas': 70,
    'Santa Cruz de Tenerife': 68, 'Paphos': 65, 'Limassol': 68, 'Nha Trang': 50,
    'Siargao': 30, 'El Nido': 28, 'Essaouira': 38, 'Punta Cana': 48, 'Zanzibar': 32,
    'Cuenca': 58, 'Da Lat': 45, 'Ubud': 45, 'Innsbruck': 82, 'Interlaken': 85,
    'San Cristóbal de las Casas': 42, 'Oaxaca': 50, 'Antigua Guatemala': 42,
    'Pokhara': 32, 'Luang Prabang': 30,
    'Colombo': 55, 'Accra': 38, 'Tunis': 52, 'Tangier': 48, 'Amman': 62,
    'Beirut': 72, 'Muscat': 68, 'Batumi': 48, 'Yerevan': 52, 'Vientiane': 35,
    'Yangon': 38, 'Kampala': 35, 'Addis Ababa': 32, 'Dakar': 35, 'Kathmandu': 35,
    'Bratislava': 68, 'Ljubljana': 72, 'Vilnius': 68, 'Plovdiv': 58,
    'Sofia': 62, 'Belgrade': 60, 'Sarajevo': 55, 'Tirana': 48,
    'Funchal': 68, 'Palma de Mallorca': 72,
    'Mérida': 55, 'Quito': 58, 'La Paz': 42, 'Santo Domingo': 50,
    'San Juan': 72,
    'Chiang Rai': 55, 'Ipoh': 58, 'Dumaguete': 42, 'Jeju': 78,
    'Taichung': 75, 'Vung Tau': 48,
}

# Climate Score (0-100, retiree comfort)
# Reference: Mediterranean=80-88, Tropical beach=75-85, cold/wet=40-55, extreme heat=45-55
NEW_CLIMATE = {
    'Faro': 85, 'Canggu': 80, 'Koh Samui': 78, 'Da Nang': 72, 'Hoi An': 72,
    'Hua Hin': 75, 'Puerto Vallarta': 80, 'Tulum': 82, 'Mazatlán': 78,
    'Cádiz': 84, 'Taormina': 82, 'Kotor': 75, 'Cascais': 82, 'Las Palmas': 88,
    'Santa Cruz de Tenerife': 86, 'Paphos': 82, 'Limassol': 80, 'Nha Trang': 78,
    'Siargao': 75, 'El Nido': 76, 'Essaouira': 78, 'Punta Cana': 80, 'Zanzibar': 76,
    'Cuenca': 78, 'Da Lat': 82, 'Ubud': 78, 'Innsbruck': 48, 'Interlaken': 45,
    'San Cristóbal de las Casas': 75, 'Oaxaca': 80, 'Antigua Guatemala': 82,
    'Pokhara': 70, 'Luang Prabang': 68,
    'Colombo': 72, 'Accra': 70, 'Tunis': 75, 'Tangier': 78, 'Amman': 68,
    'Beirut': 78, 'Muscat': 52, 'Batumi': 65, 'Yerevan': 60, 'Vientiane': 65,
    'Yangon': 62, 'Kampala': 75, 'Addis Ababa': 72, 'Dakar': 75, 'Kathmandu': 62,
    'Bratislava': 52, 'Ljubljana': 55, 'Vilnius': 45, 'Plovdiv': 60,
    'Sofia': 55, 'Belgrade': 58, 'Sarajevo': 52, 'Tirana': 65,
    'Funchal': 85, 'Palma de Mallorca': 84,
    'Mérida': 78, 'Quito': 72, 'La Paz': 55, 'Santo Domingo': 76,
    'San Juan': 80,
    'Chiang Rai': 72, 'Ipoh': 75, 'Dumaguete': 76, 'Jeju': 62,
    'Taichung': 72, 'Vung Tau': 76,
}

# Infrastructure Score (0-100, transit/roads/internet)
# Reference: Tokyo=95, Bangkok=68, Bali=20, European cities=60-85
NEW_INFRASTRUCTURE = {
    'Faro': 55, 'Canggu': 25, 'Koh Samui': 35, 'Da Nang': 52, 'Hoi An': 35,
    'Hua Hin': 40, 'Puerto Vallarta': 45, 'Tulum': 30, 'Mazatlán': 38,
    'Cádiz': 60, 'Taormina': 40, 'Kotor': 35, 'Cascais': 68, 'Las Palmas': 62,
    'Santa Cruz de Tenerife': 60, 'Paphos': 45, 'Limassol': 52, 'Nha Trang': 38,
    'Siargao': 15, 'El Nido': 12, 'Essaouira': 25, 'Punta Cana': 30, 'Zanzibar': 18,
    'Cuenca': 42, 'Da Lat': 35, 'Ubud': 22, 'Innsbruck': 78, 'Interlaken': 82,
    'San Cristóbal de las Casas': 28, 'Oaxaca': 35, 'Antigua Guatemala': 30,
    'Pokhara': 20, 'Luang Prabang': 22,
    'Colombo': 45, 'Accra': 35, 'Tunis': 42, 'Tangier': 48, 'Amman': 52,
    'Beirut': 42, 'Muscat': 65, 'Batumi': 45, 'Yerevan': 48, 'Vientiane': 30,
    'Yangon': 32, 'Kampala': 28, 'Addis Ababa': 30, 'Dakar': 32, 'Kathmandu': 25,
    'Bratislava': 72, 'Ljubljana': 70, 'Vilnius': 68, 'Plovdiv': 52,
    'Sofia': 62, 'Belgrade': 58, 'Sarajevo': 45, 'Tirana': 42,
    'Funchal': 55, 'Palma de Mallorca': 65,
    'Mérida': 42, 'Quito': 48, 'La Paz': 35, 'Santo Domingo': 42,
    'San Juan': 55,
    'Chiang Rai': 38, 'Ipoh': 52, 'Dumaguete': 28, 'Jeju': 72,
    'Taichung': 72, 'Vung Tau': 38,
}
