// ====== RETIREMENT NEIGHBORHOODS (Format 1) ======
// Cities that need to be ADDED to retireNeighborhoods in retire/index.html
// ~150 cities total (Group A missing + Group B new)

const retireNeighborhoodsNew = {

    // ══════════════════════════════════════════
    // NORTH AMERICA — United States
    // ══════════════════════════════════════════

    'New York': {
        'Upper West Side': { mult: 1.22, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Classic residential stretch along Central Park with museums, cafes, and green space.' },
        'Astoria': { mult: 0.88, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Diverse Queens neighborhood with excellent Greek and Middle Eastern food scenes.' },
        'Park Slope': { mult: 1.12, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Tree-lined Brooklyn streets with brownstones, boutiques, and Prospect Park access.' },
        'Brooklyn Heights': { mult: 1.18, tags: ['safe', 'walkable', 'quiet'], desc: 'Historic waterfront neighborhood with promenade views of Manhattan skyline.' },
    },
    'San Francisco': {
        'Marina District': { mult: 1.22, tags: ['walkable', 'safe', 'beach-access'], desc: 'Flat waterfront neighborhood with boutiques, joggers on the bay trail, and Golden Gate views.' },
        'Noe Valley': { mult: 1.18, tags: ['quiet', 'family-friendly', 'walkable'], desc: 'Sunny village-like enclave with stroller-friendly streets and local shops.' },
        'Sunset District': { mult: 0.88, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Foggy residential grid near Ocean Beach with Asian restaurants and low-key living.' },
        'Pacific Heights': { mult: 1.30, tags: ['safe', 'walkable', 'quiet'], desc: 'Prestigious hilltop area with grand Victorians and panoramic bay views.' },
    },
    'Los Angeles': {
        'Santa Monica': { mult: 1.28, tags: ['beach-access', 'walkable', 'safe'], desc: 'Iconic beachside city with pier, farmers market, and excellent transit for LA.' },
        'Silver Lake': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Hip eastside neighborhood with reservoir walking path, cafes, and independent shops.' },
        'Pasadena': { mult: 0.92, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Charming foothill city with Old Town dining, Caltech campus, and Rose Bowl.' },
        'Culver City': { mult: 1.05, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Revitalized arts district with studios, restaurants, and the Expo Line.' },
        'Mar Vista': { mult: 0.90, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Laid-back westside residential area with weekend farmers market and diverse dining.' },
    },
    'Chicago': {
        'Lincoln Park': { mult: 1.18, tags: ['safe', 'walkable', 'family-friendly'], desc: 'Lakefront neighborhood with zoo, conservatory, and tree-lined residential blocks.' },
        'Lakeview': { mult: 1.08, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Vibrant north-side area with Wrigley Field, dining, and lakefront trail access.' },
        'Logan Square': { mult: 0.92, tags: ['affordable', 'walkable', 'nightlife'], desc: 'Artsy northwest-side neighborhood with boulevard system and craft cocktail bars.' },
        'Hyde Park': { mult: 0.85, tags: ['affordable', 'quiet', 'walkable'], desc: 'University of Chicago enclave with museums, bookshops, and lakefront parks.' },
    },
    'Miami': {
        'Coconut Grove': { mult: 1.18, tags: ['walkable', 'safe', 'quiet'], desc: 'Lush bayside village with banyan trees, waterfront dining, and sailing clubs.' },
        'Coral Gables': { mult: 1.22, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Mediterranean-style planned city with Venetian Pool, fine dining, and tree canopy.' },
        'Brickell': { mult: 1.28, tags: ['central', 'walkable', 'nightlife'], desc: 'Urban financial district with high-rise condos, rooftop bars, and baywalk.' },
        'Little Havana': { mult: 0.78, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Culturally rich Cuban-American neighborhood with Calle Ocho and domino parks.' },
    },
    'Austin': {
        'South Congress (SoCo)': { mult: 1.18, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Eclectic avenue with live music venues, food trucks, and vintage shopping.' },
        'Zilker': { mult: 1.22, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Popular area near Barton Springs pool and expansive Zilker Park greenspace.' },
        'East Austin': { mult: 1.05, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Rapidly evolving eastside with craft breweries, galleries, and diverse food scene.' },
        'Cedar Park': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern suburb with parks, trails, and lower cost of living than central Austin.' },
    },
    'Seattle': {
        'Capitol Hill': { mult: 1.15, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Dense urban neighborhood with independent shops, coffee culture, and nightlife.' },
        'Ballard': { mult: 1.08, tags: ['walkable', 'quiet', 'safe'], desc: 'Former Scandinavian fishing village with breweries, locks, and Sunday farmers market.' },
        'Queen Anne': { mult: 1.12, tags: ['safe', 'walkable', 'quiet'], desc: 'Hilltop neighborhood with Space Needle views, local shops, and residential calm.' },
        'Beacon Hill': { mult: 0.85, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Diverse hillside community with light rail access, gardens, and neighborhood cafes.' },
    },
    'Denver': {
        'Cherry Creek': { mult: 1.28, tags: ['safe', 'walkable', 'central'], desc: 'Upscale shopping district with creek trail, galleries, and fine dining.' },
        'Highlands': { mult: 1.15, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Trendy northwest neighborhood with LoHi restaurants and mountain views.' },
        'Washington Park': { mult: 1.10, tags: ['quiet', 'safe', 'walkable'], desc: 'Park-centered residential area with flower gardens, lakes, and jogging paths.' },
        'Park Hill': { mult: 0.88, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Tree-lined eastern neighborhood with diverse community and local coffee shops.' },
    },
    'Boston': {
        'Back Bay': { mult: 1.30, tags: ['central', 'walkable', 'safe'], desc: 'Victorian brownstone district with Newbury Street shopping and Charles River Esplanade.' },
        'Cambridge (Harvard Sq)': { mult: 1.18, tags: ['walkable', 'safe', 'expat-friendly'], desc: 'Academic hub with bookstores, international dining, and riverside walking paths.' },
        'Jamaica Plain': { mult: 0.88, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Diverse neighborhood with Jamaica Pond, Arnold Arboretum, and local breweries.' },
        'Brookline': { mult: 1.12, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Independent town within Boston with excellent schools, parks, and Coolidge Corner.' },
    },
    'Washington DC': {
        'Georgetown': { mult: 1.30, tags: ['walkable', 'safe', 'central'], desc: 'Historic waterfront district with cobblestone streets, boutiques, and canal towpath.' },
        'Dupont Circle': { mult: 1.22, tags: ['central', 'walkable', 'nightlife'], desc: 'Embassy row neighborhood with bookshops, galleries, and Sunday farmers market.' },
        'Capitol Hill': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Row-house neighborhood near the Capitol with Eastern Market and local pubs.' },
        'Cleveland Park': { mult: 1.08, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Leafy upper northwest enclave with art deco cinema and neighborhood restaurants.' },
        'Petworth': { mult: 0.88, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Gentrifying neighborhood with growing restaurant scene and Metro access.' },
    },
    'Houston': {
        'The Heights': { mult: 1.15, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Historic bungalow district with bike trail, antique shops, and local eateries.' },
        'Montrose': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Eclectic inner-loop neighborhood with galleries, museums, and diverse dining.' },
        'Museum District': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'Cultural hub with world-class museums, Hermann Park, and the Medical Center nearby.' },
        'Katy': { mult: 0.80, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Western suburb with master-planned communities, good schools, and Asian dining.' },
    },
    'Charlotte': {
        'South End': { mult: 1.22, tags: ['walkable', 'central', 'nightlife'], desc: 'Rail trail corridor with breweries, restaurants, and light rail access.' },
        'Dilworth': { mult: 1.18, tags: ['safe', 'walkable', 'family-friendly'], desc: 'Historic trolley suburb with tree canopy, East Boulevard shops, and park access.' },
        'NoDa': { mult: 1.08, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Arts district with galleries, live music venues, and converted mill spaces.' },
        'Ballantyne': { mult: 0.88, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Suburban village center with golf courses, corporate campuses, and dining.' },
    },
    'Las Vegas': {
        'Summerlin': { mult: 1.25, tags: ['safe', 'quiet', 'mountain-views'], desc: 'Master-planned community at Red Rock Canyon base with trails and village centers.' },
        'Henderson': { mult: 1.08, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Separate city south of the Strip with parks, shopping, and desert scenery.' },
        'Downtown (Fremont)': { mult: 0.88, tags: ['central', 'walkable', 'nightlife'], desc: 'Revitalized arts district with Container Park, murals, and vintage Vegas charm.' },
        'Southern Highlands': { mult: 1.12, tags: ['safe', 'quiet', 'mountain-views'], desc: 'Gated golf community on the southern edge with mountain panoramas.' },
    },
    'Tampa': {
        'Hyde Park': { mult: 1.22, tags: ['walkable', 'safe', 'central'], desc: 'Historic neighborhood with SoHo Village restaurants and Bayshore Boulevard waterfront.' },
        'Seminole Heights': { mult: 0.92, tags: ['affordable', 'walkable', 'quiet'], desc: 'Bungalow neighborhood with craft breweries, local cafes, and community gardens.' },
        'South Tampa': { mult: 1.18, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Established residential area with Bayshore jogging path and Palma Ceia shopping.' },
        'St. Petersburg (Downtown)': { mult: 1.10, tags: ['walkable', 'beach-access', 'safe'], desc: 'Waterfront downtown across the bay with museums, murals, and pier district.' },
    },
    'Raleigh': {
        'Downtown': { mult: 1.15, tags: ['central', 'walkable', 'nightlife'], desc: 'Revitalized core with warehouse district dining, museums, and Fayetteville Street.' },
        'North Hills': { mult: 1.10, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Mixed-use midtown village with shopping, dining, and movie theater.' },
        'Five Points': { mult: 1.05, tags: ['walkable', 'quiet', 'safe'], desc: 'Charming historic neighborhood with local shops and tree-lined streets.' },
        'Cary': { mult: 0.85, tags: ['affordable', 'safe', 'family-friendly'], desc: 'Suburban town with top-rated schools, greenway trails, and diverse dining.' },
    },
    'Dallas': {
        'Uptown': { mult: 1.25, tags: ['central', 'walkable', 'nightlife'], desc: 'Walkable urban village with Katy Trail, McKinney Avenue restaurants, and bars.' },
        'Bishop Arts District': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'safe'], desc: 'Creative enclave in Oak Cliff with independent galleries, boutiques, and cafes.' },
        'Lakewood': { mult: 1.12, tags: ['safe', 'quiet', 'family-friendly'], desc: 'East Dallas neighborhood with White Rock Lake, jogging trails, and local dining.' },
        'Frisco': { mult: 0.85, tags: ['affordable', 'safe', 'family-friendly'], desc: 'Northern suburb with new development, sports venues, and excellent schools.' },
    },
    'Atlanta': {
        'Midtown': { mult: 1.18, tags: ['walkable', 'central', 'safe'], desc: 'Cultural hub with Piedmont Park, High Museum, and BeltLine trail access.' },
        'Virginia-Highland': { mult: 1.12, tags: ['walkable', 'safe', 'quiet'], desc: 'Village atmosphere with independent shops, restaurants, and bungalow homes.' },
        'Decatur': { mult: 1.05, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Independent city with courthouse square, craft beer scene, and MARTA access.' },
        'East Atlanta Village': { mult: 0.88, tags: ['affordable', 'walkable', 'nightlife'], desc: 'Eclectic neighborhood hub with dive bars, live music, and casual dining.' },
    },
    'Philadelphia': {
        'Rittenhouse Square': { mult: 1.28, tags: ['central', 'walkable', 'safe'], desc: 'Premier park-centered neighborhood with sidewalk dining and upscale townhouses.' },
        'Fishtown': { mult: 1.10, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Former industrial area turned creative hub with breweries and concert venues.' },
        'Chestnut Hill': { mult: 1.15, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Garden district at city edge with cobblestone main street and Wissahickon trails.' },
        'South Philadelphia': { mult: 0.82, tags: ['affordable', 'walkable', 'central'], desc: 'Italian Market neighborhood with cheesesteak shops, row houses, and local character.' },
    },
    'Phoenix': {
        'Scottsdale (Old Town)': { mult: 1.28, tags: ['walkable', 'safe', 'nightlife'], desc: 'Desert resort town center with galleries, spas, and upscale Southwestern dining.' },
        'Arcadia': { mult: 1.18, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Lush mid-century neighborhood at Camelback Mountain base with citrus trees.' },
        'Downtown Phoenix': { mult: 1.05, tags: ['central', 'walkable', 'nightlife'], desc: 'Revitalized urban core with Roosevelt Row murals, light rail, and First Fridays.' },
        'Tempe': { mult: 0.88, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'University town with Tempe Town Lake, Mill Avenue shops, and light rail.' },
    },
    'San Diego': {
        'La Jolla': { mult: 1.32, tags: ['beach-access', 'safe', 'quiet'], desc: 'Coastal jewel with tide pools, sea caves, upscale dining, and ocean panoramas.' },
        'North Park': { mult: 1.08, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Urban village with craft breweries, taco shops, and independent boutiques.' },
        'Hillcrest': { mult: 1.05, tags: ['walkable', 'central', 'nightlife'], desc: 'Diverse central neighborhood with Balboa Park access, farmers market, and cafes.' },
        'Pacific Beach': { mult: 1.12, tags: ['beach-access', 'walkable', 'nightlife'], desc: 'Classic surf neighborhood with boardwalk, beach bars, and casual coastal living.' },
        'Chula Vista': { mult: 0.78, tags: ['affordable', 'family-friendly', 'quiet'], desc: 'Southern suburb with bayfront parks, nature center, and cross-border culture.' },
    },
    'Nashville': {
        '12South': { mult: 1.22, tags: ['walkable', 'safe', 'expat-friendly'], desc: 'Trendy neighborhood strip with boutiques, murals, and Sevier Park green space.' },
        'East Nashville': { mult: 1.10, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Creative east-bank area with live music, farm-to-table dining, and Five Points.' },
        'The Gulch': { mult: 1.25, tags: ['central', 'walkable', 'nightlife'], desc: 'Former rail yard turned upscale urban district with hotels and rooftop bars.' },
        'Germantown': { mult: 1.15, tags: ['walkable', 'safe', 'central'], desc: 'Historic north Nashville area with brick sidewalks, restaurants, and Bicentennial Park.' },
        'Bellevue': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Western suburb along the Harpeth River with parks, trails, and chain dining.' },
    },
    'Minneapolis': {
        'Uptown': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Lakeside urban village with Chain of Lakes, bike paths, and restaurant row.' },
        'North Loop': { mult: 1.18, tags: ['central', 'walkable', 'nightlife'], desc: 'Warehouse district with craft breweries, lofts, and riverfront park access.' },
        'Linden Hills': { mult: 1.08, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Small-town feel on Lake Harriet with independent shops and walking paths.' },
        'Northeast (Nordeast)': { mult: 0.92, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Arts district with Eastern European heritage, breweries, and studio galleries.' },
        'St. Paul (Grand Ave)': { mult: 0.88, tags: ['affordable', 'walkable', 'safe'], desc: 'Victorian avenue across the river with bookshops, cafes, and Summit Avenue mansions.' },
    },
    'Portland': {
        'Pearl District': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Converted warehouse district with Powell Books, galleries, and waterfront park.' },
        'Hawthorne': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'quiet'], desc: 'Southeast corridor with vintage shops, cafes, and Mount Tabor park nearby.' },
        'Alberta Arts District': { mult: 1.05, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Northeast Portland street with galleries, street art, and Last Thursday art walks.' },
        'Sellwood': { mult: 0.92, tags: ['quiet', 'walkable', 'family-friendly'], desc: 'Antique Row neighborhood on the Willamette River with Oaks Bottom wildlife refuge.' },
        'St. Johns': { mult: 0.82, tags: ['affordable', 'quiet', 'walkable'], desc: 'Cathedral Park neighborhood with bridge views, local pubs, and small-town feel.' },
    },

    // ══════════════════════════════════════════
    // NORTH AMERICA — Canada
    // ══════════════════════════════════════════

    'Toronto': {
        'The Annex': { mult: 1.15, tags: ['walkable', 'safe', 'central'], desc: 'University-adjacent Victorian neighborhood with indie bookshops and diverse dining.' },
        'Leslieville': { mult: 1.05, tags: ['walkable', 'family-friendly', 'expat-friendly'], desc: 'East-end main street with brunch spots, boutiques, and lakefront access.' },
        'Yorkville': { mult: 1.35, tags: ['central', 'walkable', 'safe'], desc: 'Upscale shopping district with galleries, designer stores, and heritage lanes.' },
        'High Park': { mult: 1.02, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Residential area around Toronto largest park with zoo, trails, and cherry blossoms.' },
        'Scarborough (Bluffs)': { mult: 0.78, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Eastern suburb with dramatic lakeshore bluffs, parks, and multicultural food.' },
    },
    'Vancouver': {
        'Kitsilano': { mult: 1.18, tags: ['beach-access', 'walkable', 'safe'], desc: 'West-side beach neighborhood with outdoor pool, yoga culture, and mountain views.' },
        'Gastown': { mult: 1.22, tags: ['central', 'walkable', 'nightlife'], desc: 'Historic cobblestone district with steam clock, design studios, and craft cocktails.' },
        'Main Street (Mount Pleasant)': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'safe'], desc: 'Craft brewery corridor with independent shops and diverse restaurant scene.' },
        'North Vancouver': { mult: 1.05, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Mountain-base community with hiking trails, Lonsdale Quay, and SeaBus commute.' },
        'East Vancouver (Commercial Dr)': { mult: 0.88, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Italian-rooted strip with coffee houses, ethnic grocers, and community parks.' },
    },
    'Montreal': {
        'Le Plateau-Mont-Royal': { mult: 1.12, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Colorful row-house neighborhood with outdoor staircases, cafes, and park life.' },
        'Mile End': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Creative quarter with bagel shops, record stores, and bilingual street culture.' },
        'Outremont': { mult: 1.18, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Francophone residential area with tree-lined avenues and Parc Outremont.' },
        'Verdun': { mult: 0.85, tags: ['affordable', 'walkable', 'beach-access'], desc: 'Riverside neighborhood with urban beach, bike path, and Wellington Street dining.' },
    },

    // ══════════════════════════════════════════
    // EUROPE — Western & Central
    // ══════════════════════════════════════════

    'London': {
        'Richmond': { mult: 1.15, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Thames-side borough with royal deer park, botanical gardens, and village pubs.' },
        'Hampstead': { mult: 1.30, tags: ['safe', 'quiet', 'walkable'], desc: 'Hilltop village with wild heath, literary heritage, and elegant Georgian homes.' },
        'Bermondsey': { mult: 1.10, tags: ['walkable', 'central', 'expat-friendly'], desc: 'South Bank area with food markets, galleries, and Thames path walking.' },
        'Islington': { mult: 1.18, tags: ['walkable', 'central', 'nightlife'], desc: 'Canal-side borough with Upper Street restaurants, pubs, and antiques passage.' },
        'Greenwich': { mult: 0.92, tags: ['affordable', 'walkable', 'safe'], desc: 'Maritime heritage town with observatory hill, market, and parkland views.' },
    },
    'Paris': {
        'Le Marais (3rd/4th)': { mult: 1.28, tags: ['central', 'walkable', 'nightlife'], desc: 'Historic quarter with medieval streets, museums, and Place des Vosges.' },
        'Montmartre (18th)': { mult: 1.08, tags: ['walkable', 'central', 'quiet'], desc: 'Hilltop village with Sacré-Cœur views, artist studios, and vineyard.' },
        'Saint-Germain (6th)': { mult: 1.35, tags: ['central', 'walkable', 'safe'], desc: 'Literary Left Bank with legendary cafes, bookshops, and Luxembourg Gardens.' },
        'Batignolles (17th)': { mult: 1.02, tags: ['quiet', 'walkable', 'family-friendly'], desc: 'Village-like northern quarter with organic market and Martin Luther King park.' },
        'Belleville (20th)': { mult: 0.85, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Multicultural hilltop with panoramic views, Asian cuisine, and street art.' },
    },
    'Amsterdam': {
        'Jordaan': { mult: 1.25, tags: ['central', 'walkable', 'safe'], desc: 'Canal-laced former working-class quarter with galleries, cafes, and hidden courtyards.' },
        'De Pijp': { mult: 1.12, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Bohemian neighborhood with Albert Cuyp market and multicultural street life.' },
        'Oud-Zuid': { mult: 1.28, tags: ['safe', 'walkable', 'quiet'], desc: 'Museum quarter with Vondelpark, Concertgebouw, and elegant residential streets.' },
        'Amsterdam-Noord': { mult: 0.88, tags: ['affordable', 'quiet', 'expat-friendly'], desc: 'Creative waterfront across the IJ with NDSM wharf and ferry commute.' },
    },
    'Berlin': {
        'Prenzlauer Berg': { mult: 1.12, tags: ['family-friendly', 'walkable', 'safe'], desc: 'Gentrified east neighborhood with playgrounds, brunch culture, and Mauerpark.' },
        'Charlottenburg': { mult: 1.18, tags: ['safe', 'walkable', 'central'], desc: 'West Berlin elegance with Ku-damm shopping, palace gardens, and opera house.' },
        'Kreuzberg': { mult: 1.05, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Multicultural hotspot along Landwehr Canal with Turkish markets and club scene.' },
        'Schöneberg': { mult: 1.02, tags: ['walkable', 'quiet', 'safe'], desc: 'Residential west-central area with Winterfeldtplatz market and independent shops.' },
        'Neukölln': { mult: 0.85, tags: ['affordable', 'expat-friendly', 'nightlife'], desc: 'Rapidly changing southern district with diverse food scene and bar culture.' },
    },
    'Munich': {
        'Schwabing': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'University quarter with English Garden access, art galleries, and Leopoldstraße cafes.' },
        'Maxvorstadt': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Museum district with Pinakothek galleries, university buildings, and beer gardens.' },
        'Haidhausen': { mult: 1.10, tags: ['walkable', 'safe', 'quiet'], desc: 'French Quarter of Munich with Wiener Platz market and Isar riverside paths.' },
        'Sendling': { mult: 0.92, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Southern residential area with Großmarkthalle food market and local Bavarian pubs.' },
    },
    'Dublin': {
        'Ranelagh': { mult: 1.18, tags: ['walkable', 'safe', 'central'], desc: 'Village-like south Dublin with Luas tram access, gastropubs, and tree-lined roads.' },
        'Dún Laoghaire': { mult: 1.10, tags: ['safe', 'beach-access', 'walkable'], desc: 'Coastal town with harbor pier walks, seafood restaurants, and DART rail.' },
        'Howth': { mult: 1.08, tags: ['beach-access', 'quiet', 'safe'], desc: 'Fishing village peninsula with cliff walks, harbor seals, and seafood markets.' },
        'Rathmines': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'Inner south suburb with Victorian architecture, canal walks, and diverse dining.' },
        'Stoneybatter': { mult: 0.92, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Up-and-coming village with craft pubs, coffee shops, and Phoenix Park nearby.' },
    },
    'Brussels': {
        'Ixelles': { mult: 1.18, tags: ['walkable', 'expat-friendly', 'central'], desc: 'Cosmopolitan commune with Place Flagey, African quarter, and Matongé dining.' },
        'Saint-Gilles': { mult: 1.05, tags: ['walkable', 'expat-friendly', 'affordable'], desc: 'Art Nouveau gem with Parvis de Saint-Gilles bars and diverse market streets.' },
        'Uccle': { mult: 1.15, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Leafy southern commune with Bois de la Cambre forest and international schools.' },
        'Etterbeek': { mult: 1.08, tags: ['central', 'walkable', 'safe'], desc: 'EU quarter-adjacent residential area with Cinquantenaire Park and local shops.' },
        'Schaerbeek': { mult: 0.85, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Multicultural commune with cherry blossom park and Art Deco architecture.' },
    },
    'Luxembourg City': {
        'Grund': { mult: 1.22, tags: ['central', 'walkable', 'quiet'], desc: 'Historic lower town in the Alzette valley with riverside cafes and abbey ruins.' },
        'Belair': { mult: 1.28, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Upscale residential area with municipal park, embassies, and green spaces.' },
        'Bonnevoie': { mult: 0.92, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Multicultural southern quarter with train station access and diverse restaurants.' },
        'Kirchberg': { mult: 1.15, tags: ['central', 'safe', 'walkable'], desc: 'EU institutions plateau with Philharmonie, MUDAM museum, and modern architecture.' },
    },
    'Zurich': {
        'Seefeld': { mult: 1.25, tags: ['walkable', 'safe', 'beach-access'], desc: 'Lakeside neighborhood with opera house, Badi swimming spots, and upscale dining.' },
        'Niederdorf': { mult: 1.20, tags: ['central', 'walkable', 'nightlife'], desc: 'Old Town pedestrian quarter with guild houses, bars, and Limmat river views.' },
        'Wipkingen': { mult: 1.05, tags: ['walkable', 'quiet', 'safe'], desc: 'Hillside residential area with Viadukt market hall and brewery restaurants.' },
        'Oerlikon': { mult: 0.88, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Northern district with international community, convention center, and MFO park.' },
    },
    'Geneva': {
        'Eaux-Vives': { mult: 1.18, tags: ['walkable', 'central', 'safe'], desc: 'Left-bank neighborhood with lakefront park, boutiques, and farmers market.' },
        'Carouge': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Sardinian-influenced bohemian quarter with artisan workshops and piazza cafes.' },
        'Champel': { mult: 1.25, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Hilltop residential area with Arve river walks and proximity to hospitals.' },
        'Plainpalais': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'University district with Wednesday flea market, MAMCO museum, and diverse food.' },
    },
    'Edinburgh': {
        'Stockbridge': { mult: 1.15, tags: ['walkable', 'safe', 'quiet'], desc: 'Village-like enclave with Sunday market, Water of Leith path, and delis.' },
        'Morningside': { mult: 1.12, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Leafy south Edinburgh suburb with independent shops and Blackford Hill walks.' },
        'New Town': { mult: 1.25, tags: ['central', 'walkable', 'safe'], desc: 'Georgian architecture with Princes Street gardens and Queen Street shopping.' },
        'Leith': { mult: 0.88, tags: ['affordable', 'walkable', 'nightlife'], desc: 'Former port with Michelin-star dining, waterfront bars, and creative spaces.' },
    },
    'Nice': {
        'Vieux Nice (Old Town)': { mult: 1.22, tags: ['central', 'walkable', 'beach-access'], desc: 'Baroque old quarter with Cours Saleya flower market and seaside promenade.' },
        'Cimiez': { mult: 1.15, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Hilltop residential area with Matisse Museum, Roman ruins, and olive groves.' },
        'Port': { mult: 1.08, tags: ['walkable', 'central', 'beach-access'], desc: 'Harbor neighborhood with antique dealers, waterfront cafes, and Cocoa Beach.' },
        'Libération': { mult: 0.92, tags: ['affordable', 'walkable', 'central'], desc: 'Local market quarter with daily produce hall and authentic Niçois restaurants.' },
    },
    'Milan': {
        'Brera': { mult: 1.30, tags: ['central', 'walkable', 'safe'], desc: 'Art district with Pinacoteca gallery, cobblestone streets, and aperitivo bars.' },
        'Navigli': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Canal district with Sunday antique market, bars, and artist studios.' },
        'Isola': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Bohemian neighborhood near Porta Nuova towers with vintage shops and trattorias.' },
        'Città Studi': { mult: 0.88, tags: ['affordable', 'walkable', 'quiet'], desc: 'University area with Lambrate design district, ethnic food, and green spaces.' },
    },

    // ══════════════════════════════════════════
    // EUROPE — Nordics
    // ══════════════════════════════════════════

    'Stockholm': {
        'Södermalm': { mult: 1.15, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Hipster island with vintage shops, Fotografiska museum, and waterfront views.' },
        'Östermalm': { mult: 1.30, tags: ['safe', 'central', 'walkable'], desc: 'Upscale east-side with Saluhall food market and Djurgården park access.' },
        'Kungsholmen': { mult: 1.08, tags: ['walkable', 'quiet', 'safe'], desc: 'Island neighborhood with waterfront promenades, local restaurants, and city hall.' },
        'Vasastan': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Residential quarter with Odenplan hub, bakeries, and Stadsbiblioteket library.' },
        'Årsta': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Southern residential area with nature reserve and community center.' },
    },
    'Copenhagen': {
        'Nørrebro': { mult: 1.05, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Multicultural quarter with Assistens Cemetery park, street food, and bar scene.' },
        'Vesterbro': { mult: 1.12, tags: ['walkable', 'nightlife', 'central'], desc: 'Former meatpacking district with craft beer bars, boutiques, and Meatpacking food hall.' },
        'Frederiksberg': { mult: 1.18, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Garden municipality with royal gardens, zoo, and elegant apartment blocks.' },
        'Østerbro': { mult: 1.15, tags: ['safe', 'quiet', 'walkable'], desc: 'Leafy residential area with Fælledparken, harbor baths, and family atmosphere.' },
        'Amager (Islands Brygge)': { mult: 0.92, tags: ['affordable', 'beach-access', 'walkable'], desc: 'Waterfront area with harbor swimming, Amager Beach Park, and bike paths.' },
    },
    'Helsinki': {
        'Kallio': { mult: 1.05, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Working-class-turned-hip area with dive bars, saunas, and Hakaniemi market.' },
        'Töölö': { mult: 1.15, tags: ['central', 'quiet', 'safe'], desc: 'Bay-side residential area with Sibelius Park, opera house, and Olympic Stadium.' },
        'Punavuori (Design District)': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Design shops, galleries, and cafes in south Helsinki near harbor and parks.' },
        'Kruununhaka': { mult: 1.12, tags: ['central', 'walkable', 'quiet'], desc: 'Historic grid district with Senate Square, cathedral, and waterfront dining.' },
        'Lauttasaari': { mult: 0.92, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Island suburb connected by metro with beaches, nature trails, and community feel.' },
    },
    'Oslo': {
        'Grünerløkka': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Akerselva riverside neighborhood with vintage shops, parks, and Sunday markets.' },
        'Frogner': { mult: 1.28, tags: ['safe', 'quiet', 'walkable'], desc: 'West-end elegance with Vigeland sculpture park, embassies, and Bogstadveien shopping.' },
        'Majorstuen': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Commercial crossroads near Frogner Park with cafes, cinema, and transit hub.' },
        'St. Hanshaugen': { mult: 1.08, tags: ['walkable', 'quiet', 'safe'], desc: 'Hilltop park neighborhood with panoramic city views and local bakeries.' },
        'Tøyen': { mult: 0.88, tags: ['affordable', 'walkable', 'central'], desc: 'Diverse eastern quarter with Munch Museum, botanical garden, and food halls.' },
    },
    'Vienna': {
        'Innere Stadt (1st District)': { mult: 1.35, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO old town with Ringstraße, opera house, and Habsburg palaces.' },
        'Neubau (7th District)': { mult: 1.12, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Creative quarter with MuseumsQuartier, independent boutiques, and Spittelberg lanes.' },
        'Josefstadt (8th District)': { mult: 1.08, tags: ['central', 'walkable', 'quiet'], desc: 'Smallest district with Theater in der Josefstadt, cozy cafes, and antique shops.' },
        'Döbling (19th District)': { mult: 1.10, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Wine village suburb with Heurigen taverns, Vienna Woods trails, and Kahlenberg views.' },
        'Favoriten (10th District)': { mult: 0.78, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Multicultural southern district with Böhmischer Prater park and ethnic food markets.' },
    },

    // ══════════════════════════════════════════
    // ASIA — East Asia
    // ══════════════════════════════════════════

    'Tokyo': {
        'Shimokitazawa': { mult: 1.05, tags: ['walkable', 'quiet', 'expat-friendly'], desc: 'Bohemian village atmosphere with vintage shops, small theaters, and cozy cafes.' },
        'Meguro': { mult: 1.18, tags: ['safe', 'quiet', 'walkable'], desc: 'Upscale residential ward with cherry blossom river, museums, and refined dining.' },
        'Kichijoji': { mult: 1.02, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Popular west-side town with Inokashira Park, jazz bars, and shopping arcades.' },
        'Asakusa': { mult: 0.92, tags: ['affordable', 'walkable', 'central'], desc: 'Historic temple district with traditional shops, street food, and Sumida River.' },
        'Setagaya': { mult: 1.08, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Largest residential ward with Todoroki Valley, local parks, and quiet lanes.' },
    },
    'Osaka': {
        'Namba / Shinsaibashi': { mult: 1.22, tags: ['central', 'walkable', 'nightlife'], desc: 'Entertainment hub with Dotonbori canal, street food stalls, and shopping arcades.' },
        'Umeda / Kita': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Business district with department stores, sky gardens, and transit hub access.' },
        'Tennoji': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'Southern hub with Abeno Harukas tower, Shinsekai retro quarter, and zoo.' },
        'Fukushima': { mult: 1.08, tags: ['walkable', 'safe', 'quiet'], desc: 'Trendy residential area near Nakanoshima with hidden izakayas and river walks.' },
        'Sakai': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Southern neighbor city with ancient burial mounds, knife tradition, and temples.' },
    },
    'Fukuoka': {
        'Tenjin': { mult: 1.18, tags: ['central', 'walkable', 'nightlife'], desc: 'Downtown shopping and dining district with department stores and yatai food stalls.' },
        'Daimyo': { mult: 1.12, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Trendy side-street area with independent boutiques, cafes, and gallery spaces.' },
        'Ohori Park': { mult: 1.08, tags: ['quiet', 'walkable', 'safe'], desc: 'Lakeside residential area with jogging paths, Japanese garden, and art museum.' },
        'Hakata': { mult: 1.05, tags: ['central', 'walkable', 'safe'], desc: 'Station district with Canal City mall, ramen street, and temple walks.' },
        'Nishi-jin': { mult: 0.85, tags: ['affordable', 'walkable', 'quiet'], desc: 'Western residential area with Momochi seaside park and relaxed atmosphere.' },
    },
    'Seoul': {
        'Itaewon / Hannam': { mult: 1.22, tags: ['expat-friendly', 'walkable', 'nightlife'], desc: 'International district with diverse restaurants, rooftop cafes, and Namsan proximity.' },
        'Mapo-gu (Mangwon)': { mult: 1.05, tags: ['walkable', 'expat-friendly', 'affordable'], desc: 'Han River neighborhood with trendy cafes, local markets, and cycling paths.' },
        'Seongbuk-dong': { mult: 1.10, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Hillside literary village below Bukhansan Mountain with gardens and galleries.' },
        'Gangnam': { mult: 1.30, tags: ['central', 'walkable', 'safe'], desc: 'Affluent southern district with premium shopping, clinics, and COEX underground.' },
        'Eunpyeong-gu': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Northwestern residential area with Bukhansan trail access and new town development.' },
    },
    'Hong Kong': {
        'Mid-Levels': { mult: 1.28, tags: ['central', 'walkable', 'safe'], desc: 'Hillside residential zone with escalator access, harbor views, and consulate row.' },
        'Sai Kung': { mult: 0.92, tags: ['quiet', 'beach-access', 'safe'], desc: 'Eastern waterfront town with hiking trails, island beaches, and seafood restaurants.' },
        'Kennedy Town': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'affordable'], desc: 'Western island neighborhood with MTR access, waterfront promenade, and local markets.' },
        'Stanley': { mult: 1.10, tags: ['beach-access', 'quiet', 'safe'], desc: 'Southern seaside village with market, temple, and colonial heritage buildings.' },
    },
    'Taipei': {
        'Da-an District': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Tree-lined avenues with Yongkang Street food, Da-an Forest Park, and boutiques.' },
        'Tianmu': { mult: 1.12, tags: ['expat-friendly', 'safe', 'quiet'], desc: 'Northern expat enclave with American School, international grocers, and hiking.' },
        'Zhongshan': { mult: 1.08, tags: ['walkable', 'central', 'nightlife'], desc: 'Creative corridor with lanes of independent shops, galleries, and Japanese eateries.' },
        'Beitou': { mult: 0.88, tags: ['quiet', 'mountain-views', 'affordable'], desc: 'Hot spring district with sulfur valley, hiking trails, and traditional bathhouses.' },
    },
    'Shanghai': {
        'Former French Concession': { mult: 1.28, tags: ['walkable', 'expat-friendly', 'safe'], desc: 'Tree-lined colonial streets with art deco villas, boutique cafes, and jazz bars.' },
        'Jing-An': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Upscale central district with temple gardens, Nanjing West luxury, and parks.' },
        'Pudong (Lujiazui)': { mult: 1.18, tags: ['central', 'safe', 'family-friendly'], desc: 'Modern skyline district with riverside promenade, malls, and international schools.' },
        'Hongkou': { mult: 0.92, tags: ['affordable', 'walkable', 'central'], desc: 'Historic northern quarter with Jewish heritage sites, parks, and local food stalls.' },
    },
    'Beijing': {
        'Sanlitun': { mult: 1.25, tags: ['expat-friendly', 'central', 'nightlife'], desc: 'Embassy area with international dining, Taikooli shopping, and rooftop bars.' },
        'Dongcheng (Gulou)': { mult: 1.18, tags: ['central', 'walkable', 'expat-friendly'], desc: 'Hutong quarter near Drum Tower with hidden cafes, courtyard hotels, and temples.' },
        'Chaoyang (CBD)': { mult: 1.22, tags: ['central', 'safe', 'walkable'], desc: 'Business core with CCTV tower, Solana mall, and Liangma River dining strip.' },
        'Haidian (Wudaokou)': { mult: 0.88, tags: ['affordable', 'expat-friendly', 'walkable'], desc: 'University district with diverse student dining, Old Summer Palace, and tech parks.' },
    },
    'Shenzhen': {
        'Nanshan (Shekou)': { mult: 1.22, tags: ['expat-friendly', 'safe', 'beach-access'], desc: 'Coastal expat hub with Sea World plaza, ferry terminal, and international schools.' },
        'Futian CBD': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Financial center with civic square, shopping malls, and cross-border metro access.' },
        'OCT / Huaqiao Cheng': { mult: 1.12, tags: ['walkable', 'quiet', 'safe'], desc: 'Creative park district with galleries, loft cafes, and theme park access.' },
        'Longgang (Dapeng)': { mult: 0.78, tags: ['affordable', 'beach-access', 'quiet'], desc: 'Eastern peninsula with pristine beaches, geopark, and slower seaside life.' },
    },
    'Guangzhou': {
        'Tianhe': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Modern CBD with Canton Tower, Zhujiang New Town, and riverside park promenade.' },
        'Yuexiu': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'Historic heart with Shamian Island, Baiyun Mountain, and traditional dim sum halls.' },
        'Haizhu (Canton Tower area)': { mult: 1.12, tags: ['walkable', 'safe', 'central'], desc: 'Riverside district with wetland park, art museums, and Pearl River views.' },
        'Panyu': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Southern suburb with Chimelong parks, university town, and affordable apartments.' },
    },
    'Singapore': {
        'Tiong Bahru': { mult: 1.15, tags: ['walkable', 'safe', 'expat-friendly'], desc: 'Art deco heritage estate with indie bookshops, hawker center, and brunch cafes.' },
        'Holland Village': { mult: 1.12, tags: ['expat-friendly', 'walkable', 'nightlife'], desc: 'Expat enclave with al fresco dining, boutiques, and proximity to Botanic Gardens.' },
        'Katong / Joo Chiat': { mult: 1.05, tags: ['walkable', 'safe', 'expat-friendly'], desc: 'Peranakan heritage quarter with colorful shophouses, laksa stalls, and East Coast Park.' },
        'Bukit Timah': { mult: 1.22, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Upscale green-belt area near nature reserve with international schools and dining.' },
        'Geylang': { mult: 0.82, tags: ['affordable', 'walkable', 'central'], desc: 'Gritty but authentic district with legendary late-night food and Malay heritage.' },
    },
    'Manila': {
        'Makati (Legaspi Village)': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Financial center with Sunday market, Ayala Triangle gardens, and nightlife.' },
        'BGC (Bonifacio Global City)': { mult: 1.28, tags: ['safe', 'walkable', 'expat-friendly'], desc: 'Modern planned district with art installations, parks, and international dining.' },
        'Alabang': { mult: 1.05, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Southern gated community area with malls, golf courses, and suburban calm.' },
        'Quezon City (Maginhawa)': { mult: 0.85, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'University-belt food street with affordable eats, craft beer, and local culture.' },
    },
    'Jakarta': {
        'Kemang': { mult: 1.18, tags: ['expat-friendly', 'safe', 'nightlife'], desc: 'Upscale expat neighborhood with international restaurants, galleries, and bars.' },
        'Menteng': { mult: 1.25, tags: ['central', 'safe', 'quiet'], desc: 'Prestigious colonial-era district with tree-lined streets and diplomatic residences.' },
        'Pondok Indah': { mult: 1.15, tags: ['safe', 'family-friendly', 'quiet'], desc: 'Gated residential area with golf course, malls, and international hospital.' },
        'Kebayoran Baru': { mult: 1.08, tags: ['central', 'walkable', 'safe'], desc: 'Planned suburb with Blok M market, wide boulevards, and local dining.' },
        'Tangerang Selatan (BSD City)': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Satellite city with planned townships, schools, and modern commercial districts.' },
    },
    'Mumbai': {
        'Bandra West': { mult: 1.28, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Trendy suburb with Bandstand promenade, boutique restaurants, and Bollywood culture.' },
        'Colaba': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Southern tip with Gateway of India, art galleries, and Causeway shopping.' },
        'Powai': { mult: 1.05, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Lake-side IT hub with Hiranandani gardens, malls, and modern infrastructure.' },
        'Andheri West': { mult: 0.92, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Bustling suburban center with Versova beach, film studios, and diverse food.' },
    },
    'Bangalore': {
        'Indiranagar': { mult: 1.22, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Trendy east-side with 12th Main dining strip, metro access, and pub culture.' },
        'Koramangala': { mult: 1.15, tags: ['walkable', 'expat-friendly', 'nightlife'], desc: 'Startup hub with rooftop cafes, coworking spaces, and diverse restaurants.' },
        'Whitefield': { mult: 1.08, tags: ['safe', 'family-friendly', 'quiet'], desc: 'Eastern IT corridor with tech parks, international schools, and gated communities.' },
        'Jayanagar': { mult: 1.02, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Planned residential area with shopping complex, parks, and South Indian dining.' },
        'Yelahanka': { mult: 0.80, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern suburb near air force base with lakes, new apartments, and green space.' },
    },
    'Delhi': {
        'Defence Colony': { mult: 1.22, tags: ['safe', 'central', 'walkable'], desc: 'South Delhi enclave with market restaurants, parks, and metro connectivity.' },
        'Hauz Khas': { mult: 1.15, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Village complex with ruins overlooking lake, designer boutiques, and nightlife.' },
        'Greater Kailash': { mult: 1.18, tags: ['safe', 'central', 'walkable'], desc: 'Upscale south Delhi colony with M Block Market dining and boutique shopping.' },
        'Vasant Kunj': { mult: 0.92, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Southern residential area near malls, Aravalli ridge, and Qutub Minar complex.' },
        'Dwarka': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Planned southwest sub-city with wide roads, metro line, and affordable housing.' },
    },
    'Chennai': {
        'Adyar': { mult: 1.12, tags: ['safe', 'quiet', 'family-friendly'], desc: 'South Chennai neighborhood near Besant Nagar beach with educational institutions.' },
        'Nungambakkam': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Commercial hub with restaurants, consulates, and proximity to Boat Club area.' },
        'ECR (East Coast Road)': { mult: 1.08, tags: ['beach-access', 'quiet', 'expat-friendly'], desc: 'Coastal stretch with surf schools, beach resorts, and seafood shacks.' },
        'T. Nagar': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Shopping district with silk saree stores, South Indian restaurants, and temples.' },
        'Porur': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Western suburb with lake views, IT parks, and growing residential development.' },
    },

    // ══════════════════════════════════════════
    // OCEANIA
    // ══════════════════════════════════════════

    'Sydney': {
        'Surry Hills': { mult: 1.15, tags: ['walkable', 'central', 'nightlife'], desc: 'Inner-city village with laneway cafes, galleries, and diverse restaurant scene.' },
        'Bondi': { mult: 1.25, tags: ['beach-access', 'walkable', 'expat-friendly'], desc: 'Iconic beach suburb with coastal walk, surf culture, and weekend markets.' },
        'Newtown': { mult: 1.02, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Alternative inner-west hub with King Street dining, vintage shops, and live music.' },
        'Manly': { mult: 1.12, tags: ['beach-access', 'safe', 'quiet'], desc: 'Northern beaches peninsula with ferry commute, surf, and Corso promenade.' },
        'Marrickville': { mult: 0.88, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Vietnamese-Greek enclave with warehouse breweries and diverse cheap eats.' },
    },
    'Melbourne': {
        'Fitzroy': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Brunswick Street bohemia with rooftop bars, street art, and vintage shopping.' },
        'St Kilda': { mult: 1.08, tags: ['beach-access', 'walkable', 'nightlife'], desc: 'Bayside suburb with Luna Park, Acland Street cakes, and sunset pier walks.' },
        'Carlton': { mult: 1.10, tags: ['walkable', 'central', 'safe'], desc: 'Italian quarter with Lygon Street dining, university campus, and Royal Exhibition Building.' },
        'South Yarra': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'Upscale area with Chapel Street fashion, Royal Botanic Gardens, and Prahran Market.' },
        'Footscray': { mult: 0.82, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Multicultural western hub with Vietnamese food, African grocers, and market hall.' },
    },
    'Perth': {
        'Fremantle': { mult: 1.08, tags: ['walkable', 'beach-access', 'expat-friendly'], desc: 'Port city with cappuccino strip, weekend markets, and maritime heritage.' },
        'Subiaco': { mult: 1.15, tags: ['walkable', 'safe', 'central'], desc: 'Leafy inner suburb with Rokeby Road cafes, Subiaco Oval, and heritage homes.' },
        'Cottesloe': { mult: 1.22, tags: ['beach-access', 'safe', 'quiet'], desc: 'Premium beachside suburb with sculptures by the sea and Norfolk pine-lined shore.' },
        'Northbridge': { mult: 1.02, tags: ['central', 'walkable', 'nightlife'], desc: 'Cultural precinct with Chinatown, bars, art galleries, and Perth Cultural Centre.' },
        'Scarborough': { mult: 0.88, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Northern beach suburb with redeveloped foreshore, pool, and surf lifesaving club.' },
    },
    'Auckland': {
        'Ponsonby': { mult: 1.22, tags: ['walkable', 'safe', 'nightlife'], desc: 'Trendy strip with restored villas, brunch cafes, and cocktail bars.' },
        'Devonport': { mult: 1.12, tags: ['safe', 'quiet', 'beach-access'], desc: 'Heritage naval village with ferry commute, volcanic viewpoints, and galleries.' },
        'Grey Lynn': { mult: 1.08, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Inner-west neighborhood with Grey Lynn Park, organic shops, and diverse dining.' },
        'Mission Bay': { mult: 1.15, tags: ['beach-access', 'safe', 'walkable'], desc: 'Eastern waterfront with sandy beach, fountain plaza, and Rangitoto Island views.' },
        'Mt Albert': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Central-west suburb with good schools, volcanic cones, and suburban village shops.' },
    },

    // ══════════════════════════════════════════
    // MIDDLE EAST
    // ══════════════════════════════════════════

    'Abu Dhabi': {
        'Saadiyat Island': { mult: 1.30, tags: ['beach-access', 'safe', 'quiet'], desc: 'Cultural island with Louvre Abu Dhabi, pristine beaches, and luxury villas.' },
        'Corniche': { mult: 1.22, tags: ['central', 'walkable', 'beach-access'], desc: 'Waterfront promenade district with parks, cycling paths, and city skyline views.' },
        'Al Reem Island': { mult: 1.12, tags: ['safe', 'walkable', 'expat-friendly'], desc: 'Modern residential island with towers, marina mall, and waterfront dining.' },
        'Khalifa City': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Suburban community near airport with villas, schools, and community malls.' },
    },
    'Doha': {
        'The Pearl-Qatar': { mult: 1.35, tags: ['safe', 'walkable', 'beach-access'], desc: 'Man-made island with marina towers, Qanat Quartier, and waterfront promenade.' },
        'West Bay': { mult: 1.25, tags: ['central', 'walkable', 'safe'], desc: 'Skyscraper district with Corniche views, luxury hotels, and business towers.' },
        'Katara Cultural Village': { mult: 1.18, tags: ['safe', 'walkable', 'beach-access'], desc: 'Cultural hub with amphitheater, galleries, beach, and artisan workshops.' },
        'Al Wakra': { mult: 0.82, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Southern coastal town with souq, heritage village, and family-friendly waterfront.' },
    },
    'Riyadh': {
        'Al Olaya': { mult: 1.25, tags: ['central', 'walkable', 'safe'], desc: 'Financial district along King Fahd Road with Kingdom Tower and upscale malls.' },
        'Diplomatic Quarter (DQ)': { mult: 1.30, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Embassy enclave with Wadi Hanifah nature, international schools, and green spaces.' },
        'Al Nakheel': { mult: 1.12, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Northern residential area with malls, parks, and family-oriented community.' },
        'Al Malaz': { mult: 0.88, tags: ['affordable', 'central', 'walkable'], desc: 'Historic central neighborhood with King Fahd Stadium and local souq shopping.' },
    },
    'Tel Aviv': {
        'Neve Tzedek': { mult: 1.30, tags: ['walkable', 'safe', 'central'], desc: 'Restored first neighborhood with Suzanne Dellal dance center and boutique lanes.' },
        'Florentin': { mult: 1.05, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Street-art district with indie cafes, bars, and young creative energy.' },
        'Old North (Basel Area)': { mult: 1.18, tags: ['central', 'walkable', 'beach-access'], desc: 'Central residential strip with Basel Street dining, parks, and beach proximity.' },
        'Jaffa': { mult: 1.08, tags: ['walkable', 'beach-access', 'expat-friendly'], desc: 'Ancient port city with flea market, galleries, and mixed Arab-Jewish culture.' },
        'Ramat Aviv': { mult: 1.22, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Northern university area with Eretz Israel Museum, park, and upscale living.' },
    },
    'Cairo': {
        'Zamalek': { mult: 1.28, tags: ['safe', 'walkable', 'expat-friendly'], desc: 'Nile island neighborhood with embassies, galleries, opera house, and riverfront.' },
        'Maadi': { mult: 1.12, tags: ['safe', 'expat-friendly', 'quiet'], desc: 'Southern expat suburb with tree-lined streets, international schools, and Nile corniche.' },
        'Heliopolis': { mult: 1.08, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Historic eastern district with Baron Palace, wide boulevards, and airport proximity.' },
        'New Cairo (Fifth Settlement)': { mult: 1.15, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Modern eastern suburb with compounds, American University campus, and malls.' },
        'Downtown (Wust El Balad)': { mult: 0.85, tags: ['central', 'walkable', 'affordable'], desc: 'Belle Epoque center with Tahrir Square, bookshops, and classic Egyptian cafes.' },
    },
    'Nairobi': {
        'Karen': { mult: 1.22, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Leafy suburb with Blixen Museum, giraffe center, and Ngong Hills backdrop.' },
        'Westlands': { mult: 1.15, tags: ['central', 'expat-friendly', 'walkable'], desc: 'Commercial hub with Sarit Centre, international dining, and UN compound nearby.' },
        'Lavington': { mult: 1.10, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Residential area with tree-lined streets, embassies, and Lavington Mall.' },
        'Kilimani': { mult: 1.08, tags: ['central', 'walkable', 'safe'], desc: 'Central neighborhood with Yaya Centre, restaurants, and proximity to Uhuru Park.' },
        'South B': { mult: 0.82, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Middle-class residential area with community feel, churches, and local markets.' },
    },
    'Lagos': {
        'Victoria Island': { mult: 1.30, tags: ['central', 'safe', 'expat-friendly'], desc: 'Commercial island with Eko Atlantic, upscale dining, and beach clubs.' },
        'Ikoyi': { mult: 1.25, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Exclusive residential island with embassies, golf course, and waterfront living.' },
        'Lekki Phase 1': { mult: 1.15, tags: ['safe', 'family-friendly', 'quiet'], desc: 'Planned estate with shopping malls, conservation center, and gated communities.' },
        'Yaba': { mult: 0.82, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Tech hub nicknamed Yabacon Valley with startups, markets, and university campus.' },
    },

    // ══════════════════════════════════════════
    // LATIN AMERICA (Group A remaining)
    // ══════════════════════════════════════════

    'São Paulo': {
        'Vila Madalena': { mult: 1.15, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Bohemian quarter with street art, samba bars, and independent gallery scene.' },
        'Jardins (Jardim Paulista)': { mult: 1.30, tags: ['safe', 'central', 'walkable'], desc: 'Upscale tree-lined streets with Oscar Freire shopping and Paulista Avenue culture.' },
        'Pinheiros': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Creative hub with Mercado Municipal de Pinheiros, craft beer, and gastronomy.' },
        'Moema': { mult: 1.18, tags: ['safe', 'quiet', 'walkable'], desc: 'Residential neighborhood near Ibirapuera Park with bistros and boutiques.' },
        'Bela Vista (Bixiga)': { mult: 0.88, tags: ['affordable', 'central', 'walkable'], desc: 'Italian-heritage area with cantinas, theaters, and proximity to Paulista Avenue.' },
    },
    'Montevideo': {
        'Pocitos': { mult: 1.15, tags: ['beach-access', 'walkable', 'safe'], desc: 'Premier beach neighborhood with rambla promenade, cafes, and apartment living.' },
        'Punta Carretas': { mult: 1.22, tags: ['safe', 'walkable', 'beach-access'], desc: 'Upscale coastal area with lighthouse, shopping mall, and rocky shoreline walks.' },
        'Ciudad Vieja': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'Historic old town with art deco buildings, Mercado del Puerto, and port views.' },
        'Parque Rodó': { mult: 0.92, tags: ['walkable', 'quiet', 'affordable'], desc: 'Bohemian area near namesake park with university, cafes, and weekend fairs.' },
    },
    'Santiago': {
        'Providencia': { mult: 1.18, tags: ['walkable', 'safe', 'central'], desc: 'Commercial avenue district with metro access, restaurants, and Cerro San Cristóbal.' },
        'Las Condes': { mult: 1.28, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Affluent eastern commune with Costanera Center, Andes views, and international schools.' },
        'Lastarria / Bellas Artes': { mult: 1.12, tags: ['walkable', 'central', 'nightlife'], desc: 'Cultural quarter with museums, indie cinemas, and sidewalk cafes.' },
        'Ñuñoa': { mult: 1.02, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Residential middle-class area with Plaza Ñuñoa, theaters, and craft beer scene.' },
        'La Reina': { mult: 0.88, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Eastern foothill commune with nature access, parks, and residential tranquility.' },
    },
    'Guadalajara': {
        'Chapultepec / Americana': { mult: 1.15, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Avenue corridor with art deco buildings, restaurants, and craft cocktail bars.' },
        'Providencia': { mult: 1.18, tags: ['safe', 'walkable', 'central'], desc: 'Tree-lined residential area with Avenida Providencia shops and family dining.' },
        'Tlaquepaque': { mult: 0.92, tags: ['walkable', 'affordable', 'family-friendly'], desc: 'Artisan pueblo with blown glass, pottery, and pedestrian shopping streets.' },
        'Zapopan Centro': { mult: 0.88, tags: ['affordable', 'walkable', 'central'], desc: 'Religious and commercial center with basilica, markets, and metro access.' },
        'Colonia Lafayette': { mult: 1.10, tags: ['walkable', 'safe', 'quiet'], desc: 'Central residential colony with local bakeries, parks, and French-influenced architecture.' },
    },

    // ══════════════════════════════════════════════════════════
    // GROUP B — NEW CITIES (all need retirement neighborhoods)
    // ══════════════════════════════════════════════════════════

    // -- Portugal / Spain / Mediterranean --
    'Faro': {
        'Centro Histórico': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Walled old town with cathedral, cobblestone streets, and harbor marina views.' },
        'Montenegro': { mult: 0.88, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Residential area near university campus with local shops and green spaces.' },
        'Gambelas': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'University district with nature reserve access and affordable apartment living.' },
        'Praia de Faro': { mult: 1.15, tags: ['beach-access', 'quiet', 'safe'], desc: 'Barrier island beach with seafood restaurants and Ria Formosa lagoon views.' },
    },
    'Cascais': {
        'Centro de Cascais': { mult: 1.22, tags: ['walkable', 'beach-access', 'safe'], desc: 'Charming town center with marina, pedestrian streets, and coastal promenade.' },
        'Estoril': { mult: 1.18, tags: ['safe', 'beach-access', 'quiet'], desc: 'Resort town with casino gardens, Tamariz beach, and train connection to Lisbon.' },
        'Guincho': { mult: 1.08, tags: ['beach-access', 'quiet', 'mountain-views'], desc: 'Wild Atlantic beach area at Sintra Natural Park edge with surf and sunsets.' },
        'Parede': { mult: 0.88, tags: ['affordable', 'beach-access', 'quiet'], desc: 'Residential coastal town with therapeutic beach and local cafes.' },
    },
    'Funchal': {
        'Zona Velha (Old Town)': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Painted-door art district with waterfront restaurants and Mercado dos Lavradores.' },
        'Lido': { mult: 1.10, tags: ['walkable', 'beach-access', 'safe'], desc: 'Tourist promenade area with lido pools, hotels, and ocean-view dining.' },
        'São Martinho': { mult: 0.92, tags: ['affordable', 'quiet', 'safe'], desc: 'Residential hillside with Forum Madeira mall and panoramic bay views.' },
        'Monte': { mult: 0.88, tags: ['quiet', 'mountain-views', 'safe'], desc: 'Hilltop village with tropical garden, cable car, and traditional toboggan rides.' },
    },
    'Las Palmas': {
        'Triana': { mult: 1.12, tags: ['walkable', 'central', 'safe'], desc: 'Shopping and cultural corridor with pedestrian Calle Mayor and Vegueta old town nearby.' },
        'Las Canteras': { mult: 1.18, tags: ['beach-access', 'walkable', 'expat-friendly'], desc: 'Urban beach strip with Paseo promenade, surf schools, and waterfront dining.' },
        'Vegueta': { mult: 1.05, tags: ['central', 'walkable', 'quiet'], desc: 'Historic colonial quarter with cathedral, Columbus museum, and tapas bars.' },
        'Tafira': { mult: 0.88, tags: ['quiet', 'mountain-views', 'safe'], desc: 'Green hillside residential area with university, botanical garden, and cooler climate.' },
    },
    'Santa Cruz de Tenerife': {
        'Centro': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'City center with Auditorio, Garcia Sanabria park, and Calle Castillo shopping.' },
        'La Laguna': { mult: 1.05, tags: ['walkable', 'safe', 'quiet'], desc: 'UNESCO university town with colonial architecture and year-round mild climate.' },
        'El Médano': { mult: 0.92, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Southern surf town with Montaña Roja nature reserve and wind-sport culture.' },
        'Los Cristianos': { mult: 1.08, tags: ['beach-access', 'expat-friendly', 'walkable'], desc: 'Southern resort with harbor, beach promenade, and established expat community.' },
    },
    'Palma de Mallorca': {
        'Old Town': { mult: 1.25, tags: ['central', 'walkable', 'safe'], desc: 'Medieval cathedral quarter with courtyard patios, tapas, and art galleries.' },
        'Santa Catalina': { mult: 1.18, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Market neighborhood with Mercat de Santa Catalina, bars, and gallery scene.' },
        'Portixol': { mult: 1.12, tags: ['beach-access', 'quiet', 'safe'], desc: 'Former fishing village with waterfront cycling path and boutique cafes.' },
        'Son Espanyolet': { mult: 0.92, tags: ['affordable', 'walkable', 'quiet'], desc: 'Residential area near Bellver Castle with local shops and playground parks.' },
    },
    'Cádiz': {
        'Casco Antiguo': { mult: 1.15, tags: ['central', 'walkable', 'beach-access'], desc: 'Ancient walled peninsula with Playa de la Caleta, cathedral, and tapas alleys.' },
        'La Viña': { mult: 1.05, tags: ['walkable', 'affordable', 'beach-access'], desc: 'Carnival neighborhood with La Caleta beach, family-run bars, and local character.' },
        'Bahía Blanca': { mult: 0.88, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Modern residential area on the mainland side with shopping centers and parks.' },
        'El Puerto de Santa María': { mult: 0.85, tags: ['affordable', 'beach-access', 'quiet'], desc: 'Across-the-bay town with sherry bodegas, river promenade, and Playa Valdelagrana.' },
    },
    'Taormina': {
        'Centro Storico': { mult: 1.30, tags: ['walkable', 'safe', 'mountain-views'], desc: 'Hilltop town with Greek theater, Corso Umberto shopping, and Etna panoramas.' },
        'Mazzarò': { mult: 1.22, tags: ['beach-access', 'quiet', 'safe'], desc: 'Cable-car beach cove with Isola Bella nature reserve and crystal waters.' },
        'Giardini Naxos': { mult: 0.88, tags: ['beach-access', 'affordable', 'walkable'], desc: 'Seaside resort town at Taormina base with long sandy beach and boardwalk.' },
        'Castelmola': { mult: 0.82, tags: ['quiet', 'mountain-views', 'affordable'], desc: 'Tiny hilltop village above Taormina with almond wine bars and coast views.' },
    },
    'Kotor': {
        'Old Town': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO walled town with Venetian architecture, cats, and medieval church squares.' },
        'Dobrota': { mult: 0.92, tags: ['quiet', 'walkable', 'beach-access'], desc: 'Waterfront village stretching along the bay with stone houses and small beaches.' },
        'Perast': { mult: 1.05, tags: ['quiet', 'safe', 'beach-access'], desc: 'Tiny Baroque hamlet with church islands, stone palaces, and bay reflections.' },
        'Tivat': { mult: 1.10, tags: ['walkable', 'safe', 'beach-access'], desc: 'Marina town with Porto Montenegro yacht hub, boutiques, and beach clubs.' },
    },
    'Paphos': {
        'Kato Paphos': { mult: 1.15, tags: ['walkable', 'beach-access', 'expat-friendly'], desc: 'Coastal archaeological zone with harbor castle, mosaics, and waterfront tavernas.' },
        'Peyia (Coral Bay)': { mult: 1.05, tags: ['beach-access', 'quiet', 'expat-friendly'], desc: 'Resort village with sandy Coral Bay beach and established British expat community.' },
        'Chloraka': { mult: 0.88, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Residential coastal area north of Paphos with sea views and peaceful atmosphere.' },
        'Paphos Town (Ktima)': { mult: 0.92, tags: ['walkable', 'affordable', 'central'], desc: 'Upper town with covered market, local shops, and municipal gardens.' },
    },
    'Limassol': {
        'Old Town': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Castle quarter with narrow lanes, artisan workshops, and traditional tavernas.' },
        'Molos Promenade': { mult: 1.22, tags: ['walkable', 'beach-access', 'safe'], desc: 'Seafront sculpture park with jogging path, cafes, and marina views.' },
        'Germasogeia': { mult: 1.08, tags: ['beach-access', 'expat-friendly', 'walkable'], desc: 'Tourist strip area with Dasoudi beach, restaurants, and international community.' },
        'Mesa Geitonia': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Inland residential neighborhood with local markets, schools, and community parks.' },
    },

    // -- Southeast Asia --
    'Canggu': {
        'Berawa': { mult: 1.18, tags: ['beach-access', 'expat-friendly', 'nightlife'], desc: 'Booming beach area with surf breaks, beach clubs, and co-working spaces.' },
        'Batu Bolong': { mult: 1.22, tags: ['beach-access', 'walkable', 'expat-friendly'], desc: 'Central Canggu strip with cafes, yoga studios, and Old Man surf break.' },
        'Pererenan': { mult: 0.92, tags: ['quiet', 'beach-access', 'affordable'], desc: 'Northern extension with rice field views, quieter beaches, and emerging cafes.' },
        'Tanah Lot Area': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Inland area near iconic sea temple with rice terraces and village tranquility.' },
    },
    'Ubud': {
        'Central Ubud': { mult: 1.15, tags: ['walkable', 'central', 'expat-friendly'], desc: 'Cultural heart with Monkey Forest, art market, and Ubud Palace performances.' },
        'Penestanan': { mult: 0.92, tags: ['quiet', 'mountain-views', 'expat-friendly'], desc: 'Artists hillside village with rice paddies, yoga retreats, and organic cafes.' },
        'Tegallalang': { mult: 0.85, tags: ['quiet', 'mountain-views', 'affordable'], desc: 'Famous rice terrace area north of Ubud with swing attractions and craft shops.' },
        'Campuhan': { mult: 1.05, tags: ['quiet', 'walkable', 'mountain-views'], desc: 'Ridge walk starting point with luxury resorts, galleries, and valley vistas.' },
    },
    'Koh Samui': {
        'Bophut (Fisherman Village)': { mult: 1.12, tags: ['beach-access', 'walkable', 'expat-friendly'], desc: 'Charming village strip with Friday night market, boutique hotels, and dining.' },
        'Chaweng': { mult: 1.18, tags: ['beach-access', 'nightlife', 'walkable'], desc: 'Main tourist beach with shopping, nightlife, and water sports facilities.' },
        'Maenam': { mult: 0.85, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Low-key northern beach with local Thai atmosphere and budget-friendly rentals.' },
        'Lamai': { mult: 0.92, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Second-largest beach area with Hin Ta Hin Yai rocks and laid-back nightlife.' },
    },
    'Da Nang': {
        'My Khe Beach': { mult: 1.15, tags: ['beach-access', 'walkable', 'safe'], desc: 'Long urban beach with seafood restaurants, surf, and modern apartment towers.' },
        'An Thuong': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'beach-access'], desc: 'Expat-popular area near beach with Western cafes, bars, and coworking spaces.' },
        'Son Tra Peninsula': { mult: 0.92, tags: ['quiet', 'beach-access', 'mountain-views'], desc: 'Forested peninsula with monkey mountain, secluded beaches, and Lady Buddha pagoda.' },
        'Hai Chau': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Downtown core with Han Market, Dragon Bridge views, and local street food.' },
    },
    'Hoi An': {
        'Old Town': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO lantern-lit quarter with tailor shops, riverside cafes, and ancient temples.' },
        'An Bang Beach': { mult: 1.08, tags: ['beach-access', 'quiet', 'expat-friendly'], desc: 'Popular expat beach strip with beachfront bars, yoga, and casual restaurants.' },
        'Cam An': { mult: 0.85, tags: ['quiet', 'affordable', 'beach-access'], desc: 'Residential area between old town and beach with rice paddies and homestays.' },
        'Cua Dai': { mult: 0.88, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Eastern beach zone with island boat trips and quieter accommodation options.' },
    },
    'Hua Hin': {
        'Town Center': { mult: 1.08, tags: ['walkable', 'central', 'safe'], desc: 'Night market town with Cicada Market, temple, and railway station heritage.' },
        'Khao Takiab': { mult: 0.92, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Southern monkey mountain area with long quiet beach and condominium living.' },
        'Cha-Am': { mult: 0.82, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Neighboring beach town with Thai weekender atmosphere and lower prices.' },
        'Pranburi': { mult: 0.88, tags: ['beach-access', 'quiet', 'safe'], desc: 'South of Hua Hin with mangrove forest, boutique resorts, and secluded beaches.' },
    },
    'Nha Trang': {
        'Tran Phu Beach': { mult: 1.15, tags: ['beach-access', 'central', 'walkable'], desc: 'Main promenade beach with seafood, beach bars, and Vinpearl cable car views.' },
        'An Vien': { mult: 1.05, tags: ['quiet', 'beach-access', 'safe'], desc: 'Southern peninsula with upscale resorts, yacht club, and secluded cove beaches.' },
        'Nha Trang Center': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Downtown grid with Dam Market, Russian restaurants, and Po Nagar Cham towers.' },
        'Cam Ranh Bay': { mult: 0.82, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Southern bay area with pristine beaches, luxury resorts, and airport proximity.' },
    },
    'Da Lat': {
        'City Center (Xuan Huong Lake)': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'Highland lake town with flower gardens, French villas, and cool year-round climate.' },
        'Ward 3 (French Quarter)': { mult: 1.05, tags: ['walkable', 'quiet', 'safe'], desc: 'Colonial hillside with pine forests, art cafes, and boutique guesthouses.' },
        'Trai Mat': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Southern outskirts with Linh Phuoc Pagoda, flower farms, and railway connection.' },
        'Cam Ly Area': { mult: 0.88, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Waterfall neighborhood with pine groves, strawberry farms, and hillside homestays.' },
    },
    'Vung Tau': {
        'Back Beach': { mult: 1.08, tags: ['beach-access', 'walkable', 'expat-friendly'], desc: 'Main tourist beach with seafood strip, beach bars, and mountain backdrop.' },
        'Front Beach': { mult: 1.12, tags: ['beach-access', 'central', 'walkable'], desc: 'City-facing beach with promenade, Christ statue hill, and colonial lighthouse.' },
        'Long Hai': { mult: 0.82, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Coastal town east of Vung Tau with uncrowded beaches and fishing village charm.' },
        'Thang Tam': { mult: 0.88, tags: ['affordable', 'walkable', 'central'], desc: 'Central residential ward with local markets, temples, and seafood restaurants.' },
    },
    'Siargao': {
        'General Luna': { mult: 1.15, tags: ['beach-access', 'expat-friendly', 'nightlife'], desc: 'Main tourist hub with Cloud 9 surf break, island bars, and coconut palms.' },
        'Dapa': { mult: 0.82, tags: ['affordable', 'quiet', 'walkable'], desc: 'Port town with local market, ferry terminal, and authentic Filipino community.' },
        'Pacifico': { mult: 0.88, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Northern surf spot with uncrowded waves, mangrove forests, and simple island life.' },
        'Santa Monica': { mult: 0.78, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Remote northern tip with pristine beaches, cliff jumping, and rural fishing hamlets.' },
    },
    'El Nido': {
        'Town Proper': { mult: 1.12, tags: ['walkable', 'beach-access', 'expat-friendly'], desc: 'Waterfront main street with island tour operators, bars, and karst cliff backdrop.' },
        'Corong-Corong': { mult: 1.02, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Southern beach area with sunset views, hammock bars, and quieter lodging.' },
        'Nacpan Beach': { mult: 0.88, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Remote twin beach with beachfront huts, coconut groves, and minimal development.' },
        'Lio Estate': { mult: 1.18, tags: ['beach-access', 'safe', 'quiet'], desc: 'Planned resort and residential area with beach club, shops, and curated dining.' },
    },
    'Dumaguete': {
        'Rizal Boulevard': { mult: 1.08, tags: ['walkable', 'central', 'beach-access'], desc: 'Seaside promenade with university town culture, cafes, and sunset views.' },
        'Bantayan Area': { mult: 0.88, tags: ['affordable', 'quiet', 'walkable'], desc: 'Residential neighborhood near Silliman University with local markets and eateries.' },
        'Dauin': { mult: 0.85, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Coastal town south of city with world-class diving, marine sanctuaries, and resorts.' },
        'Valencia': { mult: 0.78, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Mountain town with Casaroro Falls, forest trails, and cooler highland climate.' },
    },

    // -- Mexico & Central America (Group B) --
    'Puerto Vallarta': {
        'Zona Romántica': { mult: 1.18, tags: ['walkable', 'beach-access', 'nightlife'], desc: 'Cobblestone beach town center with Playa de los Muertos, galleries, and bar scene.' },
        'Marina Vallarta': { mult: 1.12, tags: ['safe', 'quiet', 'beach-access'], desc: 'Marina community with golf course, boardwalk, and lighthouse promenade.' },
        'Fluvial Vallarta': { mult: 0.88, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Inland residential area with local shops, supermarkets, and Mexican neighborhood life.' },
        'Conchas Chinas': { mult: 1.22, tags: ['beach-access', 'quiet', 'safe'], desc: 'Hillside cove south of town with private beach access and luxury residences.' },
    },
    'Tulum': {
        'Tulum Pueblo': { mult: 0.85, tags: ['affordable', 'walkable', 'expat-friendly'], desc: 'Downtown town with local taquerias, bike-friendly streets, and cenote access.' },
        'Beach Zone (Zona Hotelera)': { mult: 1.35, tags: ['beach-access', 'quiet', 'expat-friendly'], desc: 'Car-free beach road with boutique hotels, yoga retreats, and jungle dining.' },
        'La Veleta': { mult: 0.92, tags: ['affordable', 'quiet', 'expat-friendly'], desc: 'Developing residential area south of pueblo with new condos and co-working.' },
        'Aldea Zamá': { mult: 1.15, tags: ['walkable', 'safe', 'expat-friendly'], desc: 'Planned community between town and beach with modern condos and social clubs.' },
    },
    'Mazatlán': {
        'Centro Histórico': { mult: 1.05, tags: ['walkable', 'central', 'affordable'], desc: 'Restored colonial center with Plazuela Machado, Angela Peralta theater, and galleries.' },
        'Zona Dorada': { mult: 1.15, tags: ['beach-access', 'walkable', 'nightlife'], desc: 'Golden Zone tourist strip with resort hotels, beaches, and seafood restaurants.' },
        'Olas Altas': { mult: 1.08, tags: ['walkable', 'beach-access', 'central'], desc: 'Malecón promenade start with cliff diving, sunset views, and bohemian cafes.' },
        'Cerritos': { mult: 0.88, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Northern beach community with surf breaks, organic farms, and relaxed expat scene.' },
    },
    'San Cristóbal de las Casas': {
        'Centro': { mult: 1.08, tags: ['walkable', 'central', 'safe'], desc: 'Highland colonial center with Santo Domingo church, amber market, and cafes.' },
        'Barrio de Guadalupe': { mult: 0.92, tags: ['walkable', 'affordable', 'quiet'], desc: 'Hillside neighborhood with church viewpoint and local indigenous market vendors.' },
        'Real de Guadalupe': { mult: 1.02, tags: ['walkable', 'expat-friendly', 'central'], desc: 'Pedestrian street with international restaurants, hostels, and artisan shops.' },
        'Barrio de Mexicanos': { mult: 0.78, tags: ['affordable', 'quiet', 'walkable'], desc: 'Traditional barrio with hilltop church panorama and authentic local atmosphere.' },
    },
    'Oaxaca': {
        'Centro Histórico': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO colonial center with zócalo, mezcal bars, and Zapotec textile markets.' },
        'Jalatlaco': { mult: 1.08, tags: ['walkable', 'quiet', 'expat-friendly'], desc: 'Bohemian barrio with colorful houses, craft coffee shops, and community murals.' },
        'Reforma': { mult: 0.92, tags: ['walkable', 'affordable', 'central'], desc: 'Residential quarter north of center with local comedores and neighborhood parks.' },
        'Xochimilco': { mult: 1.02, tags: ['walkable', 'quiet', 'safe'], desc: 'Southern barrio with artisan workshops, mezcalerías, and local church plaza.' },
    },
    'Mérida': {
        'Centro Histórico': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'Colonial grid with pastel mansions, Paseo Montejo boulevard, and Sunday markets.' },
        'Santiago': { mult: 1.02, tags: ['walkable', 'quiet', 'affordable'], desc: 'Historic barrio with renovated colonial homes, local eateries, and church square.' },
        'Paseo de Montejo': { mult: 1.18, tags: ['walkable', 'safe', 'central'], desc: 'Grand boulevard with Porfirian mansions, museums, and sidewalk restaurants.' },
        'Chuburná': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern residential area with mercado, local life, and easy highway access.' },
    },
    'Antigua Guatemala': {
        'Centro': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO colonial town with cobblestones, Arco de Santa Catalina, and volcano views.' },
        'San Pedro Las Huertas': { mult: 0.85, tags: ['quiet', 'affordable', 'mountain-views'], desc: 'Village on Antigua outskirts with Agua volcano views and rural tranquility.' },
        'Jocotenango': { mult: 0.88, tags: ['affordable', 'quiet', 'walkable'], desc: 'Northern suburb with coffee finca museum, local market, and residential calm.' },
        'San Juan del Obispo': { mult: 0.80, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Hilltop village with panoramic valley views and traditional Guatemalan culture.' },
    },

    // -- South America (Group B) --
    'Cuenca': {
        'El Centro': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO historic core with cathedral domes, flower market, and cobblestone plazas.' },
        'El Vergel': { mult: 0.92, tags: ['walkable', 'quiet', 'affordable'], desc: 'Riverside neighborhood with Tomebamba river walk, cafes, and gallery spaces.' },
        'Gringolandia': { mult: 1.02, tags: ['expat-friendly', 'walkable', 'safe'], desc: 'Popular expat area near SuperMaxi with familiar amenities and social groups.' },
        'Misicata': { mult: 0.78, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Western outskirts with valley views, haciendas, and lower cost rural living.' },
    },
    'Quito': {
        'La Mariscal': { mult: 1.08, tags: ['central', 'walkable', 'nightlife'], desc: 'Tourist and expat hub with Plaza Foch restaurants, bars, and travel agencies.' },
        'Cumbayá': { mult: 1.18, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Eastern valley suburb with warm microclimate, malls, and international dining.' },
        'González Suárez': { mult: 1.22, tags: ['safe', 'walkable', 'central'], desc: 'Upscale avenue with valley viewpoints, high-rise condos, and fine dining.' },
        'La Floresta': { mult: 1.05, tags: ['walkable', 'quiet', 'expat-friendly'], desc: 'Bohemian neighborhood with craft coffee roasters, galleries, and quiet streets.' },
        'Cotocollao': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern residential area with local market, park, and traditional neighborhood feel.' },
    },
    'La Paz': {
        'Sopocachi': { mult: 1.12, tags: ['walkable', 'safe', 'central'], desc: 'Middle-class neighborhood with Parque Urbano, cafes, and lively Calle Guachalla.' },
        'Zona Sur (Calacoto)': { mult: 1.22, tags: ['safe', 'quiet', 'family-friendly'], desc: 'Southern valley suburb at lower altitude with malls, parks, and expat community.' },
        'San Miguel': { mult: 1.08, tags: ['safe', 'walkable', 'quiet'], desc: 'Upscale Zona Sur area with restaurants, Plaza Humboldt, and leafy streets.' },
        'El Alto (Villa Adela)': { mult: 0.72, tags: ['affordable', 'walkable', 'mountain-views'], desc: 'High-altitude city with Alasita festival, cholita culture, and Andean panoramas.' },
    },
    'Santo Domingo': {
        'Zona Colonial': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO first colonial city in the Americas with Alcázar, cathedral, and plazas.' },
        'Piantini': { mult: 1.22, tags: ['safe', 'walkable', 'central'], desc: 'Upscale embassy district with international dining, parks, and modern malls.' },
        'Gazcue': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Residential area near Malecón waterfront with art deco houses and cultural venues.' },
        'Los Jardines': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern residential zone with shopping plazas, schools, and community parks.' },
    },
    'Punta Cana': {
        'Bávaro': { mult: 1.18, tags: ['beach-access', 'safe', 'expat-friendly'], desc: 'Main resort strip with white-sand beach, shopping villages, and water sports.' },
        'Cap Cana': { mult: 1.30, tags: ['safe', 'beach-access', 'quiet'], desc: 'Luxury marina community with Jack Nicklaus golf, yacht club, and private beaches.' },
        'El Cortecito': { mult: 1.05, tags: ['beach-access', 'walkable', 'nightlife'], desc: 'Beachfront village with souvenir shops, restaurants, and catamaran excursions.' },
        'Verón': { mult: 0.78, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Service town behind resorts with Dominican local life, markets, and cheap eats.' },
    },
    'San Juan': {
        'Condado': { mult: 1.22, tags: ['beach-access', 'walkable', 'safe'], desc: 'Urban beach neighborhood with Ashford Avenue shopping, hotels, and ocean pools.' },
        'Old San Juan': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Colorful colonial fortress city with blue cobblestones, galleries, and harbor views.' },
        'Santurce': { mult: 1.05, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Arts district with La Placita market nightlife, murals, and gallery scene.' },
        'Isla Verde': { mult: 1.12, tags: ['beach-access', 'safe', 'quiet'], desc: 'Resort beach strip near airport with calm waters and beachfront condos.' },
    },

    // -- South Asia / Nepal / Sri Lanka --
    'Pokhara': {
        'Lakeside': { mult: 1.10, tags: ['walkable', 'expat-friendly', 'mountain-views'], desc: 'Tourist strip along Phewa Lake with Annapurna views, cafes, and boat rentals.' },
        'Dam Side': { mult: 0.88, tags: ['affordable', 'walkable', 'quiet'], desc: 'Quieter lake end with local restaurants, dam viewpoint, and budget lodging.' },
        'Sedi Height': { mult: 0.82, tags: ['quiet', 'mountain-views', 'affordable'], desc: 'Hillside neighborhood with panoramic Himalayan views and peaceful village atmosphere.' },
        'Mahendrapul': { mult: 0.78, tags: ['affordable', 'walkable', 'central'], desc: 'Local bazaar area with authentic Nepali dining, shops, and bus station access.' },
    },
    'Kathmandu': {
        'Thamel': { mult: 1.12, tags: ['central', 'walkable', 'expat-friendly'], desc: 'Tourist quarter with trekking gear shops, rooftop restaurants, and temple walks.' },
        'Patan (Lalitpur)': { mult: 1.05, tags: ['walkable', 'safe', 'quiet'], desc: 'Ancient Newar city with Durbar Square, metalwork artisans, and courtyard cafes.' },
        'Boudhanath': { mult: 1.02, tags: ['walkable', 'quiet', 'expat-friendly'], desc: 'Tibetan Buddhist quarter around massive stupa with monasteries and momos.' },
        'Jhamsikhel': { mult: 0.92, tags: ['quiet', 'safe', 'walkable'], desc: 'Emerging restaurant area in Lalitpur with cafes, galleries, and expat community.' },
    },
    'Colombo': {
        'Colombo 3 (Kollupitiya)': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Main commercial strip with Galle Road shopping, ocean-view dining, and embassies.' },
        'Colombo 7 (Cinnamon Gardens)': { mult: 1.25, tags: ['safe', 'quiet', 'walkable'], desc: 'Embassy district with University of Colombo, museums, and tree-lined avenues.' },
        'Mount Lavinia': { mult: 0.92, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Southern beach suburb with colonial hotel heritage, surf, and seafood restaurants.' },
        'Colombo 5 (Havelock Town)': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'Residential area with Havelock City mall, local restaurants, and park access.' },
    },

    // -- East Asia (Group B) --
    'Jeju': {
        'Jeju City': { mult: 1.08, tags: ['central', 'walkable', 'safe'], desc: 'Island capital with black pork street, Dongmun Market, and airport proximity.' },
        'Seogwipo': { mult: 1.02, tags: ['walkable', 'beach-access', 'quiet'], desc: 'Southern port town with Jeungmun resort area, waterfalls, and mandarin groves.' },
        'Hallim': { mult: 0.85, tags: ['quiet', 'beach-access', 'affordable'], desc: 'Western town with Hyeopjae Beach, lava tubes, and rural village atmosphere.' },
        'Jocheon': { mult: 0.82, tags: ['quiet', 'affordable', 'mountain-views'], desc: 'Eastern area near Hallasan trails with stone wall villages and ocean panoramas.' },
    },
    'Taichung': {
        'West District': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Downtown core with Miyahara ice cream, National Taichung Theater, and night market.' },
        'Nantun District': { mult: 1.05, tags: ['safe', 'family-friendly', 'walkable'], desc: 'Residential area with Rainbow Village, IKEA, and Maple Garden heritage park.' },
        'Xitun District': { mult: 1.08, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Western district with National Museum of Natural Science and Fengjia Night Market.' },
        'Beitun District': { mult: 0.88, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Northern foothill area with Dakeng hiking trails and newer residential development.' },
    },
    'Chiang Rai': {
        'City Center': { mult: 1.05, tags: ['walkable', 'central', 'safe'], desc: 'Compact downtown with clock tower, Saturday walking street, and night bazaar.' },
        'Tha Sut': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Northern outskirts near hot springs with rural Thai countryside and tea plantations.' },
        'Rob Wiang': { mult: 0.88, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Southern area near Big C and airport with affordable condominiums and local markets.' },
        'Mae Fah Luang': { mult: 0.78, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'University area with botanical garden, mountain air, and peaceful village life.' },
    },
    'Ipoh': {
        'Old Town': { mult: 1.08, tags: ['walkable', 'central', 'safe'], desc: 'Heritage quarter with colonial shophouses, white coffee, and Concubine Lane.' },
        'New Town': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Commercial center with famous bean sprout chicken, dim sum halls, and cinemas.' },
        'Bercham': { mult: 0.85, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Residential township with hawker stalls, Buddhist temple, and community life.' },
        'Tambun': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Limestone hill area with Lost World hot springs, pomelo orchards, and cave temples.' },
    },

    // -- Africa / Middle East / Caucasus (Group B) --
    'Essaouira': {
        'Medina': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Walled wind city with blue fishing boats, artisan woodworkers, and Gnawa music.' },
        'Diabat': { mult: 0.82, tags: ['affordable', 'beach-access', 'quiet'], desc: 'Village south of town near sand dunes with surf camps and Hendrix legend.' },
        'Ghazoua': { mult: 0.78, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Northern coastal area with quieter beaches and emerging guesthouse scene.' },
        'Moulay Bouzerktoune': { mult: 0.75, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Windsurf point village north of Essaouira with Atlantic swells and simple life.' },
    },
    'Zanzibar': {
        'Stone Town': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO labyrinth with carved doors, rooftop restaurants, and Forodhani night market.' },
        'Nungwi': { mult: 1.08, tags: ['beach-access', 'expat-friendly', 'quiet'], desc: 'Northern tip with turquoise waters, dhow sailing, and sunset beach bars.' },
        'Jambiani': { mult: 0.82, tags: ['beach-access', 'affordable', 'quiet'], desc: 'Southeast coast village with seaweed farms, kite surfing, and local community.' },
        'Paje': { mult: 0.92, tags: ['beach-access', 'expat-friendly', 'affordable'], desc: 'Kite-surf paradise with white sand, budget hostels, and growing cafe scene.' },
    },
    'Accra': {
        'Osu': { mult: 1.15, tags: ['walkable', 'central', 'nightlife'], desc: 'Oxford Street hub with restaurants, bars, and vibrant Ghanaian street culture.' },
        'Cantonments': { mult: 1.22, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Embassy district with international schools, restaurants, and residential compounds.' },
        'East Legon': { mult: 1.18, tags: ['safe', 'family-friendly', 'expat-friendly'], desc: 'Upscale residential area with American International School, malls, and dining.' },
        'Labadi': { mult: 0.88, tags: ['beach-access', 'affordable', 'walkable'], desc: 'Beach neighborhood with Labadi Beach Hotel strip and oceanfront drumming circles.' },
    },
    'Tangier': {
        'Kasbah': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Hilltop fortress quarter with Strait of Gibraltar views and Dar el Makhzen museum.' },
        'Ville Nouvelle': { mult: 1.05, tags: ['central', 'walkable', 'affordable'], desc: 'French-built new town with Boulevard Pasteur cafes, cinema, and shopping.' },
        'Malabata': { mult: 0.92, tags: ['beach-access', 'quiet', 'safe'], desc: 'Eastern coastal area with sandy beach, residential towers, and marina development.' },
        'Cap Spartel': { mult: 0.85, tags: ['quiet', 'beach-access', 'mountain-views'], desc: 'Atlantic cape with lighthouse, Caves of Hercules, and dramatic coastal scenery.' },
    },
    'Amman': {
        'Abdoun': { mult: 1.22, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Upscale hillside with bridge landmark, embassy residences, and international dining.' },
        'Jabal Amman (Rainbow Street)': { mult: 1.12, tags: ['walkable', 'central', 'expat-friendly'], desc: 'First Circle area with heritage buildings, indie cafes, and city panoramas.' },
        'Sweifieh': { mult: 1.08, tags: ['walkable', 'safe', 'central'], desc: 'Commercial district with malls, restaurants, and accessible healthcare.' },
        'Tabarbour': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern residential area with new apartments, local markets, and family living.' },
    },
    'Beirut': {
        'Achrafieh': { mult: 1.22, tags: ['walkable', 'safe', 'nightlife'], desc: 'Christian quarter hilltop with Gemmayze nightlife, galleries, and Sursock Museum.' },
        'Hamra': { mult: 1.08, tags: ['central', 'walkable', 'expat-friendly'], desc: 'AUB neighborhood with bookshops, diverse restaurants, and intellectual culture.' },
        'Mar Mikhael': { mult: 1.12, tags: ['walkable', 'nightlife', 'expat-friendly'], desc: 'Former industrial strip with speakeasy bars, street art, and creative studios.' },
        'Verdun': { mult: 1.05, tags: ['safe', 'central', 'walkable'], desc: 'Shopping boulevard with ABC mall, residential towers, and city park access.' },
        'Raouche': { mult: 0.92, tags: ['walkable', 'beach-access', 'affordable'], desc: 'Corniche waterfront with Pigeon Rocks landmark, cliff cafes, and sea views.' },
    },
    'Muscat': {
        'Qurum': { mult: 1.15, tags: ['safe', 'walkable', 'beach-access'], desc: 'Central beach area with natural park, Grand Mosque nearby, and waterfront dining.' },
        'Al Mouj': { mult: 1.25, tags: ['safe', 'beach-access', 'expat-friendly'], desc: 'Planned marina development with The Wave golf, beach, and modern residences.' },
        'Mutrah': { mult: 1.05, tags: ['walkable', 'central', 'affordable'], desc: 'Historic harbor with corniche promenade, souq, and frankincense merchants.' },
        'Al Khuwair': { mult: 0.92, tags: ['affordable', 'central', 'walkable'], desc: 'Commercial area with ministries, malls, and accessible residential apartments.' },
    },
    'Batumi': {
        'Old Town': { mult: 1.10, tags: ['central', 'walkable', 'safe'], desc: 'Compact historic center with Piazza Square, cobblestone cafes, and mosques.' },
        'New Boulevard': { mult: 1.15, tags: ['walkable', 'beach-access', 'safe'], desc: 'Seafront promenade with cycling path, sculptures, and beachside restaurants.' },
        'Makhinjauri': { mult: 0.82, tags: ['affordable', 'quiet', 'beach-access'], desc: 'Southern suburb with botanical garden, quieter beaches, and hillside views.' },
        'Gonio': { mult: 0.85, tags: ['beach-access', 'quiet', 'affordable'], desc: 'Ancient fortress town south of Batumi with pebble beach and mountain backdrop.' },
    },
    'Yerevan': {
        'Kentron (Center)': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Republic Square area with Cascade steps, sidewalk cafes, and Ararat views.' },
        'Arabkir': { mult: 0.92, tags: ['quiet', 'safe', 'family-friendly'], desc: 'Residential district with Victory Park, local bakeries, and neighborhood character.' },
        'Davtashen': { mult: 0.85, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Northern hillside neighborhood with panoramic city views and growing development.' },
        'Avan': { mult: 0.78, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Eastern suburb with Hrazdan gorge views, local markets, and peaceful streets.' },
    },

    // -- Eastern Europe / Balkans (Group B) --
    'Bratislava': {
        'Staré Mesto (Old Town)': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Compact historic core with castle views, Danube promenade, and outdoor cafes.' },
        'Ružinov': { mult: 1.02, tags: ['walkable', 'safe', 'family-friendly'], desc: 'Large residential district with Štrkovecké Lake, shopping, and Eurovea access.' },
        'Petržalka': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Danube south-bank housing estate with Sad Janka Kráľa park and cycling paths.' },
        'Karlova Ves': { mult: 0.88, tags: ['quiet', 'safe', 'walkable'], desc: 'Western residential area near Devín Castle with university campus and nature trails.' },
    },
    'Ljubljana': {
        'Center': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Car-free riverside core with Triple Bridge, Plečnik market, and castle funicular.' },
        'Metelkova': { mult: 1.02, tags: ['walkable', 'central', 'nightlife'], desc: 'Former barracks turned autonomous arts quarter with galleries and live music.' },
        'Trnovo': { mult: 1.05, tags: ['quiet', 'walkable', 'safe'], desc: 'Southern residential area along Gradaščica with Plečnik church and student cafes.' },
        'Šiška': { mult: 0.85, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Northern neighborhood with Tivoli Park access, BTC shopping, and diverse dining.' },
    },
    'Vilnius': {
        'Senamiestis (Old Town)': { mult: 1.22, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO Baroque old town with courtyards, cathedral square, and Pilies Street cafes.' },
        'Užupis': { mult: 1.08, tags: ['walkable', 'expat-friendly', 'quiet'], desc: 'Self-declared artists republic across the Vilnia with galleries and bohemian spirit.' },
        'Šnipiškės': { mult: 1.02, tags: ['central', 'walkable', 'safe'], desc: 'Modern business district with Europa Tower, riverside path, and shopping centers.' },
        'Žirmūnai': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern residential area with Neris River walks, shopping, and Soviet heritage.' },
    },
    'Plovdiv': {
        'Old Town': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Painted revival houses on three hills with Roman amphitheater and art galleries.' },
        'Kapana': { mult: 1.08, tags: ['walkable', 'central', 'nightlife'], desc: 'Creative quarter with street art, craft workshops, and craft beer bars.' },
        'Trakia': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Large residential district with parks, markets, and affordable apartment living.' },
        'Tsentar': { mult: 1.02, tags: ['central', 'walkable', 'affordable'], desc: 'Main pedestrian zone with Plovdiv Main Street shopping and Roman Stadium.' },
    },
    'Sofia': {
        'Oborishte': { mult: 1.18, tags: ['central', 'walkable', 'safe'], desc: 'Upscale district with embassies, Doctor Garden park, and Nevski Cathedral nearby.' },
        'Lozenets': { mult: 1.12, tags: ['walkable', 'safe', 'central'], desc: 'South-central neighborhood with cafes, parks, and South Park greenery.' },
        'Studentski Grad': { mult: 0.78, tags: ['affordable', 'walkable', 'nightlife'], desc: 'University campus area with bars, cheap eats, and youthful energy.' },
        'Vitosha Boulevard': { mult: 1.05, tags: ['central', 'walkable', 'safe'], desc: 'Main pedestrian avenue with mountain views, shopping, and outdoor dining.' },
    },
    'Belgrade': {
        'Dorćol': { mult: 1.12, tags: ['walkable', 'central', 'nightlife'], desc: 'Oldest neighborhood with Danube riverside, street art, and craft coffee culture.' },
        'Vračar': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Residential hilltop with St. Sava Temple, Kalenić market, and cafe culture.' },
        'Stari Grad': { mult: 1.18, tags: ['central', 'walkable', 'nightlife'], desc: 'Historic center with Knez Mihailova pedestrian street and Kalemegdan fortress.' },
        'Zemun': { mult: 0.82, tags: ['affordable', 'walkable', 'quiet'], desc: 'Former Habsburg town on the Danube with Gardoš Tower, fish restaurants, and quay.' },
    },
    'Sarajevo': {
        'Baščaršija': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Ottoman bazaar quarter with copper workshops, ćevapi, and Sebilj fountain.' },
        'Marijin Dvor': { mult: 1.05, tags: ['central', 'walkable', 'safe'], desc: 'Modern center with National Museum, Holiday Inn landmark, and tram connections.' },
        'Ilidža': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Western suburb with Vrelo Bosne spring park, spa history, and mountain access.' },
        'Bistrik': { mult: 0.88, tags: ['affordable', 'walkable', 'quiet'], desc: 'Hillside mahala neighborhood with Ottoman houses, minaret views, and local bakeries.' },
    },
    'Tirana': {
        'Blloku': { mult: 1.18, tags: ['walkable', 'central', 'nightlife'], desc: 'Former communist elite quarter turned cafe and bar hotspot with colorful buildings.' },
        'Tirana e Re (New Tirana)': { mult: 1.05, tags: ['central', 'walkable', 'safe'], desc: 'Southern residential area with Grand Park lake, artificial beach, and stadium.' },
        'Ish-Blloku (21 Dhjetori)': { mult: 0.88, tags: ['affordable', 'walkable', 'quiet'], desc: 'Residential blocks with local markets, bakeries, and emerging cafe scene.' },
        'Sauk': { mult: 0.82, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Southern hillside suburb with Dajti Mountain views and expanding residential areas.' },
    },
    'Innsbruck': {
        'Altstadt (Old Town)': { mult: 1.25, tags: ['central', 'walkable', 'mountain-views'], desc: 'Golden Roof medieval center with Alpine backdrop, arcaded streets, and cafes.' },
        'Wilten': { mult: 1.08, tags: ['walkable', 'quiet', 'safe'], desc: 'Southern residential quarter with Wilten Basilica, Bergisel ski jump views, and parks.' },
        'Hötting': { mult: 1.02, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Hillside village with Nordkette cable car access, vineyards, and panoramic hiking.' },
        'Pradl': { mult: 0.88, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Eastern residential area with Sillpark shopping, local cafes, and Inn River walks.' },
    },
    'Interlaken': {
        'Interlaken West': { mult: 1.18, tags: ['central', 'walkable', 'mountain-views'], desc: 'Town center near Thunersee with Höhematte park, shops, and Jungfrau panoramas.' },
        'Unterseen': { mult: 1.05, tags: ['walkable', 'quiet', 'mountain-views'], desc: 'Old village across the Aare with timbered houses, artists quarter, and lakeside.' },
        'Matten': { mult: 0.92, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Southern village with residential calm, local dining, and Schynige Platte access.' },
        'Bönigen': { mult: 0.88, tags: ['quiet', 'safe', 'mountain-views'], desc: 'Brienzersee lakeside hamlet with swimming, waterfall hikes, and peaceful retreat.' },
    },

    // -- Southeast Asia / misc (Group B remaining) --
    'Luang Prabang': {
        'Old Town Peninsula': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'UNESCO riverside core with gilded temples, morning alms, and night market.' },
        'Ban Xieng Mouane': { mult: 0.92, tags: ['quiet', 'walkable', 'affordable'], desc: 'Temple district on the peninsula with traditional wooden houses and monastery views.' },
        'Ban Phonheuang': { mult: 0.82, tags: ['affordable', 'quiet', 'walkable'], desc: 'Southern area across Nam Khan river with local market and guesthouse scene.' },
        'Ban Phanom': { mult: 0.78, tags: ['affordable', 'quiet', 'mountain-views'], desc: 'Weaving village outside town with textile workshops and rural Lao countryside.' },
    },
    'Vientiane': {
        'Chanthabouly (Mekong Riverside)': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Downtown core with Mekong sunset promenade, night market, and French-era cafes.' },
        'Sikhottabong': { mult: 0.92, tags: ['affordable', 'quiet', 'walkable'], desc: 'Western district with That Luang stupa, morning market, and residential streets.' },
        'Sisattanak': { mult: 1.05, tags: ['central', 'walkable', 'expat-friendly'], desc: 'Diplomatic area with COPE center, international restaurants, and riverside bars.' },
        'Naxaythong': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Outer suburban area with local temples, farmland, and peaceful Lao family life.' },
    },
    'Yangon': {
        'Downtown': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Colonial grid with Sule Pagoda, Strand Hotel, and Bogyoke Aung San Market.' },
        'Bahan (Shwedagon area)': { mult: 1.18, tags: ['central', 'safe', 'quiet'], desc: 'Lake-side district with golden Shwedagon Pagoda, Inya Lake, and diplomatic residences.' },
        'Hlaing (Inya Road)': { mult: 1.05, tags: ['quiet', 'safe', 'walkable'], desc: 'University area with Inya Lake walking paths, bookshops, and garden restaurants.' },
        'Insein': { mult: 0.78, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Northern township with local markets, monasteries, and traditional neighborhood life.' },
    },
    'Kampala': {
        'Kololo': { mult: 1.22, tags: ['safe', 'quiet', 'expat-friendly'], desc: 'Hilltop diplomatic quarter with embassies, upscale dining, and garden residences.' },
        'Nakasero': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Central hill with Sheraton area, craft market, and panoramic city views.' },
        'Bugolobi': { mult: 1.05, tags: ['safe', 'walkable', 'expat-friendly'], desc: 'Eastern residential area with Game Stores mall, restaurants, and community parks.' },
        'Ntinda': { mult: 0.85, tags: ['affordable', 'walkable', 'family-friendly'], desc: 'Northern trading center with local markets, nightlife strip, and diverse community.' },
    },
    'Addis Ababa': {
        'Bole': { mult: 1.18, tags: ['central', 'walkable', 'expat-friendly'], desc: 'Airport-adjacent area with Bole Road restaurants, malls, and international community.' },
        'Old Airport (Kazanchis)': { mult: 1.12, tags: ['central', 'walkable', 'safe'], desc: 'Business district with UN headquarters, hotels, and Meskel Square nearby.' },
        'CMC / Summit': { mult: 0.88, tags: ['affordable', 'quiet', 'safe'], desc: 'Eastern residential area with condominium developments and growing commercial centers.' },
        'Sarbet': { mult: 0.82, tags: ['affordable', 'quiet', 'family-friendly'], desc: 'Western hillside neighborhood with residential calm, churches, and local markets.' },
    },
    'Dakar': {
        'Plateau': { mult: 1.15, tags: ['central', 'walkable', 'safe'], desc: 'Administrative center with Place de l Indépendance, colonial buildings, and ocean views.' },
        'Almadies': { mult: 1.22, tags: ['beach-access', 'safe', 'expat-friendly'], desc: 'Western peninsula with beach clubs, upscale restaurants, and surfing at Ngor.' },
        'Ngor': { mult: 1.08, tags: ['beach-access', 'quiet', 'safe'], desc: 'Fishing village with Ngor Island pirogue trip, surf breaks, and laid-back charm.' },
        'Ouakam': { mult: 0.85, tags: ['affordable', 'walkable', 'beach-access'], desc: 'Hillside neighborhood with Mamelles lighthouse, local fish market, and mosque views.' },
    },
    'Tunis': {
        'La Marsa': { mult: 1.15, tags: ['beach-access', 'safe', 'walkable'], desc: 'Coastal suburb with beach promenade, café terraces, and Sidi Bou Said proximity.' },
        'Sidi Bou Said': { mult: 1.22, tags: ['walkable', 'safe', 'beach-access'], desc: 'Blue-and-white clifftop village with panoramic Mediterranean views and art galleries.' },
        'Les Berges du Lac': { mult: 1.12, tags: ['safe', 'central', 'walkable'], desc: 'Modern business district around lake with malls, hotels, and embassy row.' },
        'La Goulette': { mult: 0.85, tags: ['affordable', 'walkable', 'beach-access'], desc: 'Port town with seafood restaurants, beach, and TGM train to Tunis center.' },
    },
};


// ====== SALARY CONVERTER NEIGHBORHOODS (Format 2) ======
// Only Group B new cities need these (existing cities already have them)
// 10-30 neighborhoods per city, name → multiplier

const salaryNeighborhoodsNew = {

    // -- Portugal --
    'Faro': {
        'Centro Histórico': 1.12, 'Montenegro': 0.88, 'Gambelas': 0.82,
        'Praia de Faro': 1.15, 'Penha': 0.85, 'São Luís': 0.80,
        'Alto de Santo António': 0.90, 'Estoi': 0.75, 'Santa Bárbara de Nexe': 0.78,
        'Almancil': 1.08, 'Loulé': 0.85, 'Quarteira': 0.92,
        'Vilamoura': 1.22, 'Olhão': 0.82, 'Tavira': 0.88
    },
    'Cascais': {
        'Centro de Cascais': 1.22, 'Estoril': 1.18, 'Guincho': 1.08,
        'Parede': 0.88, 'Carcavelos': 0.92, 'São Domingos de Rana': 0.82,
        'Birre': 1.05, 'Areia': 0.95, 'Alvide': 0.90,
        'Alcabideche': 0.78, 'Murches': 0.85, 'Malveira da Serra': 0.92,
        'Monte Estoril': 1.12, 'São João do Estoril': 1.02
    },
    'Funchal': {
        'Zona Velha (Old Town)': 1.15, 'Lido': 1.10, 'São Martinho': 0.92,
        'Monte': 0.88, 'Santa Luzia': 0.95, 'Santo António': 0.82,
        'São Roque': 0.85, 'Imaculado Coração de Maria': 0.88,
        'Santa Maria Maior': 1.05, 'São Pedro': 1.02, 'São Gonçalo': 0.80,
        'Câmara de Lobos': 0.75, 'Caniço': 0.78, 'Machico': 0.72
    },

    // -- Spain / Canary Islands --
    'Las Palmas': {
        'Triana': 1.12, 'Las Canteras': 1.18, 'Vegueta': 1.05,
        'Tafira': 0.88, 'Ciudad Jardín': 1.10, 'Guanarteme': 1.02,
        'Alcaravaneras': 1.08, 'Mesa y López': 1.05, 'Schamann': 0.82,
        'Tamaraceite': 0.75, 'La Isleta': 0.78, 'Arenales': 1.00,
        'Miller Bajo': 0.85, 'San Cristóbal': 0.80, 'Telde': 0.72
    },
    'Santa Cruz de Tenerife': {
        'Centro': 1.10, 'La Laguna': 1.05, 'El Médano': 0.92,
        'Los Cristianos': 1.08, 'Costa Adeje': 1.15, 'Playa de las Américas': 1.12,
        'Puerto de la Cruz': 0.98, 'La Orotava': 0.85, 'Icod de los Vinos': 0.78,
        'Guía de Isora': 0.82, 'Los Llanos': 0.80, 'Tacoronte': 0.82,
        'Candelaria': 0.78, 'Arona': 0.88, 'Garachico': 0.75
    },
    'Palma de Mallorca': {
        'Old Town': 1.25, 'Santa Catalina': 1.18, 'Portixol': 1.12,
        'Son Espanyolet': 0.92, 'El Terreno': 1.02, 'Son Armadams': 1.05,
        'La Bonanova': 1.22, 'Génova': 0.95, 'Son Rapinya': 1.08,
        'Son Sardina': 0.78, 'Coll d\'en Rabassa': 0.85, 'Playa de Palma': 1.10,
        'Illetes': 1.28, 'Es Molinar': 0.88, 'Sant Agustí': 1.15,
        'Sóller': 1.05, 'Valldemossa': 1.08, 'Alcúdia': 0.92,
        'Pollença': 0.95, 'Manacor': 0.78
    },
    'Cádiz': {
        'Casco Antiguo': 1.15, 'La Viña': 1.05, 'Bahía Blanca': 0.88,
        'El Puerto de Santa María': 0.85, 'San Fernando': 0.82,
        'Santa María': 1.08, 'Mentidero': 1.02, 'La Laguna': 0.92,
        'Chiclana de la Frontera': 0.78, 'Sanlúcar de Barrameda': 0.80,
        'Rota': 0.82, 'Jerez de la Frontera': 0.75, 'Puntales': 0.88,
        'Extramuros': 0.90
    },

    // -- Italy / Montenegro / Cyprus --
    'Taormina': {
        'Centro Storico': 1.30, 'Mazzarò': 1.22, 'Giardini Naxos': 0.88,
        'Castelmola': 0.82, 'Letojanni': 0.85, 'Spisone': 0.92,
        'Trappitello': 0.78, 'Villagonia': 0.90, 'Mazzeo': 0.88,
        'Recanati': 0.82, 'Taormina Mare': 1.10, 'Isolabella': 1.15,
        'Alcantara Valley': 0.75
    },
    'Kotor': {
        'Old Town': 1.22, 'Dobrota': 0.92, 'Perast': 1.05,
        'Tivat': 1.10, 'Porto Montenegro': 1.25, 'Risan': 0.78,
        'Prčanj': 0.85, 'Muo': 0.88, 'Stoliv': 0.80,
        'Budva': 1.08, 'Sveti Stefan': 1.30, 'Herceg Novi': 0.88
    },
    'Paphos': {
        'Kato Paphos': 1.15, 'Peyia (Coral Bay)': 1.05, 'Chloraka': 0.88,
        'Paphos Town (Ktima)': 0.92, 'Emba': 0.85, 'Tala': 0.90,
        'Mandria': 0.82, 'Geroskipou': 0.88, 'Kissonerga': 0.92,
        'Kouklia': 0.78, 'Latchi': 0.95, 'Polis Chrysochous': 0.85,
        'Tsada': 0.82, 'Mesa Chorio': 0.80
    },
    'Limassol': {
        'Old Town': 1.12, 'Molos Promenade': 1.22, 'Germasogeia': 1.08,
        'Mesa Geitonia': 0.85, 'Agios Athanasios': 0.90, 'Agios Tychonas': 1.05,
        'Polemidia': 0.78, 'Zakaki': 0.82, 'Ypsonas': 0.80,
        'Erimi': 0.75, 'Episkopi': 0.78, 'Columbia Area': 1.02,
        'Potamos Germasogeia': 0.92, 'Amathus': 1.15, 'Mouttagiaka': 1.10
    },

    // -- Southeast Asia --
    'Canggu': {
        'Berawa': 1.18, 'Batu Bolong': 1.22, 'Pererenan': 0.92,
        'Tanah Lot Area': 0.82, 'Canggu Proper': 1.05, 'Tibubeneng': 0.95,
        'Seseh': 0.88, 'Cemagi': 0.85, 'Umalas': 1.08,
        'Kerobokan': 1.02, 'Munggu': 0.78, 'Babakan': 0.90
    },
    'Ubud': {
        'Central Ubud': 1.15, 'Penestanan': 0.92, 'Tegallalang': 0.85,
        'Campuhan': 1.05, 'Sayan': 1.10, 'Kedewatan': 1.08,
        'Peliatan': 0.88, 'Nyuh Kuning': 0.95, 'Mas': 0.82,
        'Lodtunduh': 0.78, 'Keliki': 0.80, 'Payangan': 0.75,
        'Tampaksiring': 0.78
    },
    'Koh Samui': {
        'Bophut': 1.12, 'Chaweng': 1.18, 'Maenam': 0.85,
        'Lamai': 0.92, 'Chaweng Noi': 1.15, 'Bangrak': 0.95,
        'Nathon': 0.78, 'Taling Ngam': 0.88, 'Lipa Noi': 0.85,
        'Hua Thanon': 0.80, 'Choeng Mon': 1.08, 'Ban Tai': 0.82
    },
    'Da Nang': {
        'My Khe Beach': 1.15, 'An Thuong': 1.08, 'Son Tra Peninsula': 0.92,
        'Hai Chau': 1.02, 'Thanh Khe': 0.85, 'Lien Chieu': 0.78,
        'Ngu Hanh Son': 0.88, 'Cam Le': 0.82, 'Hoa Vang': 0.72,
        'Non Nuoc Beach': 1.05, 'Phuoc My': 1.10, 'Thuan Phuoc': 0.88
    },
    'Hoi An': {
        'Old Town': 1.18, 'An Bang Beach': 1.08, 'Cam An': 0.85,
        'Cua Dai': 0.88, 'Cam Thanh': 0.82, 'Tra Que': 0.78,
        'Cam Ha': 0.80, 'Tan An': 0.92, 'Son Phong': 0.85,
        'Thanh Ha': 0.78, 'Cam Chau': 0.82, 'Cam Kim Island': 0.72
    },
    'Hua Hin': {
        'Town Center': 1.08, 'Khao Takiab': 0.92, 'Cha-Am': 0.82,
        'Pranburi': 0.88, 'Nong Kae': 0.95, 'Hin Lek Fai': 0.85,
        'Bo Fai': 0.78, 'Nong Phlap': 0.75, 'Khao Tao': 0.82,
        'Sam Roi Yot': 0.72, 'Hua Hin Soi 88': 0.88, 'Hua Hin Soi 112': 0.82
    },
    'Nha Trang': {
        'Tran Phu Beach': 1.15, 'An Vien': 1.05, 'Nha Trang Center': 1.02,
        'Cam Ranh Bay': 0.82, 'Phuoc Hai': 0.88, 'Vinh Hai': 0.85,
        'Vinh Hoa': 0.80, 'Loc Tho': 0.92, 'Xuong Huan': 0.88,
        'Vinh Nguyen': 0.78, 'Bai Dai': 0.85, 'Doc Let': 0.75,
        'Ninh Hoa': 0.72
    },
    'Da Lat': {
        'City Center': 1.10, 'Ward 3': 1.05, 'Trai Mat': 0.82,
        'Cam Ly': 0.88, 'Ward 1': 1.02, 'Ward 4': 0.92,
        'Ward 5': 0.88, 'Ward 7': 0.85, 'Ward 8': 0.82,
        'Ward 9': 0.80, 'Ward 10': 0.78, 'Ward 11': 0.82,
        'Xuan Truong': 0.75, 'Ta Nung': 0.72
    },
    'Vung Tau': {
        'Back Beach': 1.08, 'Front Beach': 1.12, 'Long Hai': 0.82,
        'Thang Tam': 0.88, 'Ward 1': 1.02, 'Ward 2': 1.05,
        'Ward 5': 0.92, 'Ward 7': 0.85, 'Ward 8': 0.88,
        'Nguy Van Tho': 0.80, 'Phuoc Hai': 0.78, 'Ho Tram': 0.85
    },
    'Siargao': {
        'General Luna': 1.15, 'Dapa': 0.82, 'Pacifico': 0.88,
        'Santa Monica': 0.78, 'Cloud 9': 1.18, 'Catangnan': 0.85,
        'Union': 0.80, 'San Isidro': 0.78, 'Burgos': 0.75,
        'Del Carmen': 0.72, 'Pilar': 0.72
    },
    'El Nido': {
        'Town Proper': 1.12, 'Corong-Corong': 1.02, 'Nacpan Beach': 0.88,
        'Lio Estate': 1.18, 'Buena Suerte': 0.82, 'Marimegmeg': 1.05,
        'Aberawan': 0.78, 'Pasandigan': 0.80, 'Sibaltan': 0.72,
        'New Ibajay': 0.75, 'Taytay': 0.70, 'San Fernando': 0.72
    },
    'Dumaguete': {
        'Rizal Boulevard': 1.08, 'Bantayan Area': 0.88, 'Dauin': 0.85,
        'Valencia': 0.78, 'Piapi': 1.02, 'Daro': 0.85,
        'Taclobo': 0.82, 'Bagacay': 0.80, 'Cantil-e': 0.78,
        'Bajumpandan': 0.82, 'Cadawinonan': 0.85, 'Camanjac': 0.78,
        'Junob': 0.82, 'Looc': 0.80, 'Banilad': 0.88
    },
    'Chiang Rai': {
        'City Center': 1.05, 'Tha Sut': 0.82, 'Rob Wiang': 0.88,
        'Mae Fah Luang': 0.78, 'Wiang': 0.92, 'Rop Wiang': 0.85,
        'Rimkok': 0.80, 'Doi Hang': 0.75, 'Ban Du': 0.82,
        'San Sai': 0.78, 'Mae Chan': 0.72, 'Chiang Saen': 0.75
    },
    'Ipoh': {
        'Old Town': 1.08, 'New Town': 1.02, 'Bercham': 0.85,
        'Tambun': 0.82, 'Falim': 0.80, 'Pasir Puteh': 0.88,
        'Taman Cempaka': 0.82, 'Fair Park': 0.85, 'Tiger Lane': 0.90,
        'Greentown': 0.95, 'Meru': 0.78, 'Tanjung Rambutan': 0.72,
        'Gunung Rapat': 0.82, 'Silibin': 0.78, 'Ampang': 0.82
    },
    'Jeju': {
        'Jeju City': 1.08, 'Seogwipo': 1.02, 'Hallim': 0.85,
        'Jocheon': 0.82, 'Aewol': 0.90, 'Gujwa': 0.78,
        'Jungmun': 1.12, 'Daejeong': 0.80, 'Andeok': 0.82,
        'Hangyeong': 0.78, 'Seongsan': 0.85, 'Namwon': 0.80,
        'Pyoseon': 0.78, 'Udo Island': 0.88
    },
    'Taichung': {
        'West District': 1.12, 'Nantun District': 1.05, 'Xitun District': 1.08,
        'Beitun District': 0.88, 'Central District': 1.02, 'North District': 0.95,
        'South District': 0.90, 'East District': 0.92, 'Taiping District': 0.82,
        'Dali District': 0.78, 'Wufeng District': 0.75, 'Fengyuan District': 0.82,
        'Tanzi District': 0.80, 'Dajia District': 0.75, 'Shalu District': 0.78
    },

    // -- Mexico (Group B) --
    'Puerto Vallarta': {
        'Zona Romántica': 1.18, 'Marina Vallarta': 1.12, 'Fluvial Vallarta': 0.88,
        'Conchas Chinas': 1.22, 'Hotel Zone': 1.15, 'Versalles': 0.85,
        'Pitillal': 0.75, 'Las Juntas': 0.72, 'Nuevo Vallarta (Nayarit)': 1.10,
        'Bucerías': 0.92, 'Sayulita': 1.08, 'Mismaloya': 1.05,
        'Amapas': 1.18, 'Gringo Gulch': 1.08, 'Col. Emiliano Zapata': 0.80
    },
    'Tulum': {
        'Tulum Pueblo': 0.85, 'Beach Zone (Zona Hotelera)': 1.35, 'La Veleta': 0.92,
        'Aldea Zamá': 1.15, 'Region 15': 0.78, 'Boca Paila Road': 1.25,
        'Selvazama': 1.08, 'Holistika': 1.02, 'Tulum Norte': 0.80,
        'Francisco Uh May': 0.72, 'Akumal': 1.10, 'Tankah': 1.05,
        'Sian Ka\'an Access': 1.12
    },
    'Mazatlán': {
        'Centro Histórico': 1.05, 'Zona Dorada': 1.15, 'Olas Altas': 1.08,
        'Cerritos': 0.88, 'Marina Mazatlán': 1.12, 'Playa Brujas': 0.92,
        'Sabalo Country': 1.02, 'El Cid': 1.08, 'Lomas de Mazatlán': 0.90,
        'Sábalo Cerritos': 0.95, 'Pradera Dorada': 0.78, 'Villa Galaxia': 0.75,
        'Nuevo Mazatlán': 0.82, 'Hacienda del Mar': 0.85, 'Infonavit Playas': 0.72
    },
    'San Cristóbal de las Casas': {
        'Centro': 1.08, 'Barrio de Guadalupe': 0.92, 'Real de Guadalupe': 1.02,
        'Barrio de Mexicanos': 0.78, 'Barrio de Cuxtitali': 0.82,
        'La Garita': 0.80, 'Del Valle': 0.85, 'Las Rosas': 0.75,
        'Barrio de Tlaxcala': 0.78, 'Barrio El Cerrillo': 0.82,
        'San Ramón': 0.72, 'La Merced': 0.80
    },
    'Oaxaca': {
        'Centro Histórico': 1.12, 'Jalatlaco': 1.08, 'Reforma': 0.92,
        'Xochimilco': 1.02, 'Trinidad de las Huertas': 0.88, 'Ex-Marquesado': 0.85,
        'Volcanes': 0.78, 'Del Maestro': 0.80, 'Linda Vista': 0.82,
        'Lomas de Santa Rosa': 0.75, 'San Felipe del Agua': 0.95,
        'Donaji': 0.78, 'Presidentes': 0.72, 'Candiani': 0.75
    },
    'Mérida': {
        'Centro Histórico': 1.10, 'Santiago': 1.02, 'Paseo de Montejo': 1.18,
        'Chuburná': 0.85, 'García Ginerés': 1.05, 'Montes de Amé': 1.08,
        'Francisco de Montejo': 0.92, 'Gran Santa Fe': 0.78,
        'Altabrisa': 1.02, 'Temozon Norte': 0.88, 'Dzitya': 0.82,
        'Cholul': 0.85, 'Santa Gertrudis Copó': 0.92, 'Itzimna': 1.00,
        'Campestre': 1.05
    },

    // -- Central America (Group B) --
    'Antigua Guatemala': {
        'Centro': 1.15, 'San Pedro Las Huertas': 0.85, 'Jocotenango': 0.88,
        'San Juan del Obispo': 0.80, 'Ciudad Vieja': 0.78, 'San Felipe': 0.82,
        'Santa Ana': 0.78, 'El Calvario': 0.92, 'La Merced': 1.02,
        'San Cristóbal el Bajo': 0.75, 'Pastores': 0.72, 'Santa Lucía Milpas Altas': 0.82
    },
    'Santo Domingo': {
        'Zona Colonial': 1.12, 'Piantini': 1.22, 'Gazcue': 1.02,
        'Los Jardines': 0.85, 'Naco': 1.15, 'Bella Vista': 1.08,
        'Evaristo Morales': 1.05, 'La Julia': 1.02, 'Seralles': 1.10,
        'Arroyo Hondo': 0.88, 'Los Cacicazgos': 1.18, 'Ensanche Ozama': 0.78,
        'Villa Mella': 0.72, 'Los Ríos': 0.80, 'Villa Consuelo': 0.75,
        'Cristo Rey': 0.72, 'Alma Rosa': 0.82
    },
    'Punta Cana': {
        'Bávaro': 1.18, 'Cap Cana': 1.30, 'El Cortecito': 1.05,
        'Verón': 0.78, 'Cabeza de Toro': 1.12, 'Uvero Alto': 1.08,
        'Arena Gorda': 1.15, 'Los Corales': 0.92, 'Friusa': 0.82,
        'Higüey': 0.72, 'San Rafael del Yuma': 0.68, 'Bayahíbe': 0.88,
        'La Romana': 0.82, 'Dominicus': 0.92
    },
    'San Juan': {
        'Condado': 1.22, 'Old San Juan': 1.18, 'Santurce': 1.05,
        'Isla Verde': 1.12, 'Ocean Park': 1.15, 'Miramar': 1.08,
        'Hato Rey': 1.02, 'Río Piedras': 0.82, 'Guaynabo': 0.92,
        'Bayamón': 0.78, 'Carolina': 0.80, 'Caguas': 0.75,
        'Dorado': 1.08, 'Toa Baja': 0.72, 'Trujillo Alto': 0.78
    },

    // -- South America (Group B) --
    'Cuenca': {
        'El Centro': 1.10, 'El Vergel': 0.92, 'Gringolandia': 1.02,
        'Misicata': 0.78, 'Yanuncay': 0.85, 'El Batán': 0.95,
        'Totoracocha': 0.82, 'San Sebastián': 0.88, 'Gil Ramírez Dávalos': 0.90,
        'Barrial Blanco': 0.82, 'Challuabamba': 0.75, 'Ricaurte': 0.78,
        'Monay': 0.80, 'Sayausí': 0.72
    },
    'Quito': {
        'La Mariscal': 1.08, 'Cumbayá': 1.18, 'González Suárez': 1.22,
        'La Floresta': 1.05, 'Cotocollao': 0.82, 'Quito Tenis': 1.12,
        'La Carolina': 1.15, 'Iñaquito': 1.10, 'El Batán': 1.08,
        'Bellavista': 1.02, 'Tumbaco': 0.88, 'San Rafael': 0.85,
        'Los Chillos': 0.80, 'Pomasqui': 0.78, 'Calderón': 0.72,
        'La Vicentina': 0.88, 'La Paz': 0.92
    },
    'La Paz': {
        'Sopocachi': 1.12, 'Zona Sur (Calacoto)': 1.22, 'San Miguel': 1.08,
        'El Alto (Villa Adela)': 0.72, 'Achumani': 1.15, 'Obrajes': 1.05,
        'Miraflores': 1.02, 'San Pedro': 0.88, 'Centro': 0.92,
        'Cota Cota': 1.08, 'Irpavi': 1.05, 'Mallasa': 0.85,
        'Següencoma': 1.02, 'Villa Fátima': 0.78, 'Tembladerani': 0.82
    },

    // -- South Asia (Group B) --
    'Pokhara': {
        'Lakeside': 1.10, 'Dam Side': 0.88, 'Sedi Height': 0.82,
        'Mahendrapul': 0.78, 'Baidam': 1.02, 'Khahare': 0.85,
        'Parsyang': 0.80, 'Chipledhunga': 0.75, 'Nagdhunga': 0.78,
        'Prithvi Chowk': 0.82, 'Sarangkot': 0.88, 'Begnas': 0.72
    },
    'Kathmandu': {
        'Thamel': 1.12, 'Patan (Lalitpur)': 1.05, 'Boudhanath': 1.02,
        'Jhamsikhel': 0.92, 'Lazimpat': 1.08, 'Durbar Marg': 1.15,
        'Baluwatar': 1.05, 'Baneshwor': 0.88, 'Chabahil': 0.82,
        'Swayambhu': 0.85, 'Maharajgunj': 0.95, 'Battisputali': 0.80,
        'Koteshwor': 0.78, 'Kirtipur': 0.72, 'Bhaktapur': 0.78
    },
    'Colombo': {
        'Colombo 3 (Kollupitiya)': 1.18, 'Colombo 7 (Cinnamon Gardens)': 1.25,
        'Mount Lavinia': 0.92, 'Colombo 5 (Havelock Town)': 1.05,
        'Colombo 4 (Bambalapitiya)': 1.08, 'Colombo 6 (Wellawatte)': 0.95,
        'Dehiwala': 0.88, 'Nugegoda': 0.82, 'Rajagiriya': 0.92,
        'Battaramulla': 0.85, 'Nawala': 0.88, 'Colombo 2 (Slave Island)': 1.02,
        'Colombo 1 (Fort)': 1.12, 'Maharagama': 0.78, 'Kotte': 0.82
    },

    // -- Eastern Europe / Balkans (Group B) --
    'Bratislava': {
        'Staré Mesto (Old Town)': 1.18, 'Ružinov': 1.02, 'Petržalka': 0.78,
        'Karlova Ves': 0.88, 'Nové Mesto': 0.92, 'Dúbravka': 0.82,
        'Vajnory': 0.75, 'Podunajské Biskupice': 0.78, 'Devínska Nová Ves': 0.80,
        'Lamač': 0.85, 'Rača': 0.82, 'Vrakuňa': 0.78,
        'Čunovo': 0.72, 'Záhorská Bystrica': 0.78
    },
    'Ljubljana': {
        'Center': 1.18, 'Metelkova': 1.02, 'Trnovo': 1.05,
        'Šiška': 0.85, 'Bežigrad': 0.92, 'Moste': 0.82,
        'Vič': 0.88, 'Polje': 0.78, 'Rudnik': 0.80,
        'Šentvid': 0.82, 'Dravlje': 0.85, 'Črnuče': 0.78,
        'Rožna Dolina': 1.02
    },
    'Vilnius': {
        'Senamiestis (Old Town)': 1.22, 'Užupis': 1.08, 'Šnipiškės': 1.02,
        'Žirmūnai': 0.82, 'Antakalnis': 0.92, 'Žvėrynas': 1.05,
        'Naujamiestis': 1.08, 'Rasos': 0.88, 'Karoliniškės': 0.78,
        'Lazdynai': 0.75, 'Fabijoniškės': 0.78, 'Pilaitė': 0.80,
        'Pašilaičiai': 0.75, 'Baltupiai': 0.82
    },
    'Plovdiv': {
        'Old Town': 1.15, 'Kapana': 1.08, 'Trakia': 0.78,
        'Tsentar': 1.02, 'Komatevo': 0.82, 'Gagarin': 0.78,
        'Karshiyaka': 0.80, 'Sadiyski': 0.75, 'Stolipinovo': 0.70,
        'Mladezhki Halm': 0.82, 'Filipovo': 0.85, 'Ostromila': 0.78,
        'Proslav': 0.75
    },
    'Sofia': {
        'Oborishte': 1.18, 'Lozenets': 1.12, 'Studentski Grad': 0.78,
        'Vitosha Boulevard': 1.05, 'Iztok': 1.08, 'Krasno Selo': 0.85,
        'Mladost': 0.80, 'Lyulin': 0.72, 'Nadezhda': 0.75,
        'Ovcha Kupel': 0.78, 'Dragalevtsi': 1.02, 'Boyana': 1.10,
        'Simeonovo': 0.92, 'Bankya': 0.78, 'Manastirski Livadi': 0.88
    },
    'Belgrade': {
        'Dorćol': 1.12, 'Vračar': 1.15, 'Stari Grad': 1.18,
        'Zemun': 0.82, 'Savski Venac': 1.10, 'Novi Beograd': 0.88,
        'Čukarica': 0.78, 'Voždovac': 0.82, 'Zvezdara': 0.85,
        'Rakovica': 0.78, 'Palilula': 0.85, 'Dedinje': 1.22,
        'Senjak': 1.18, 'Banjica': 0.88, 'Karaburma': 0.78
    },
    'Sarajevo': {
        'Baščaršija': 1.12, 'Marijin Dvor': 1.05, 'Ilidža': 0.82,
        'Bistrik': 0.88, 'Čengić Vila': 0.85, 'Grbavica': 0.92,
        'Kovačići': 0.88, 'Mejtas': 1.02, 'Koševo': 0.95,
        'Otoka': 0.82, 'Alipašino Polje': 0.78, 'Dobrinja': 0.75,
        'Hrasnica': 0.72, 'Stup': 0.78
    },
    'Tirana': {
        'Blloku': 1.18, 'Tirana e Re': 1.05, 'Ish-Blloku': 0.88,
        'Sauk': 0.82, 'Komuna e Parisit': 0.92, 'Liqeni Artificial': 1.08,
        'Don Bosko': 0.78, 'Kombinat': 0.72, 'Laprakë': 0.75,
        'Selitë': 0.80, 'Kinostudio': 0.85, 'Ali Demi': 0.82,
        'Medreseja': 0.80
    },

    // -- Switzerland / Austria (Group B) --
    'Innsbruck': {
        'Altstadt (Old Town)': 1.25, 'Wilten': 1.08, 'Hötting': 1.02,
        'Pradl': 0.88, 'Saggen': 1.12, 'Reichenau': 0.85,
        'Mühlau': 0.92, 'Arzl': 0.82, 'Amras': 0.85,
        'Vill': 0.80, 'Igls': 1.05, 'Rum': 0.82,
        'Hall in Tirol': 0.78, 'Völs': 0.82
    },
    'Interlaken': {
        'Interlaken West': 1.18, 'Unterseen': 1.05, 'Matten': 0.92,
        'Bönigen': 0.88, 'Wilderswil': 0.85, 'Grindelwald': 1.15,
        'Lauterbrunnen': 1.08, 'Beatenberg': 0.82, 'Brienz': 0.82,
        'Thun': 0.88, 'Spiez': 0.85, 'Ringgenberg': 0.80
    },

    // -- Africa (Group B) --
    'Essaouira': {
        'Medina': 1.12, 'Diabat': 0.82, 'Ghazoua': 0.78,
        'Moulay Bouzerktoune': 0.75, 'Quartier des Dunes': 0.88,
        'Bab Marrakech': 1.02, 'Bab Doukkala': 0.92, 'Kasbah': 1.08,
        'Mellah': 0.85, 'Sidi Mohamed Ben Abdallah': 0.80
    },
    'Zanzibar': {
        'Stone Town': 1.18, 'Nungwi': 1.08, 'Jambiani': 0.82,
        'Paje': 0.92, 'Kendwa': 1.12, 'Matemwe': 0.88,
        'Kiwengwa': 0.85, 'Michamvi': 0.80, 'Bwejuu': 0.82,
        'Pingwe': 0.78, 'Fumba': 0.80, 'Mbweni': 0.88
    },
    'Accra': {
        'Osu': 1.15, 'Cantonments': 1.22, 'East Legon': 1.18,
        'Labadi': 0.88, 'Airport Residential': 1.15, 'Labone': 1.10,
        'Dzorwulu': 1.05, 'North Ridge': 1.02, 'Adenta': 0.78,
        'Tema': 0.75, 'Spintex': 0.82, 'Achimota': 0.80,
        'Dansoman': 0.72, 'Madina': 0.75, 'Teshie': 0.78
    },
    'Kampala': {
        'Kololo': 1.22, 'Nakasero': 1.15, 'Bugolobi': 1.05,
        'Ntinda': 0.85, 'Muyenga': 1.08, 'Naguru': 1.02,
        'Bukoto': 0.92, 'Kiwatule': 0.82, 'Namugongo': 0.75,
        'Naalya': 0.78, 'Lubowa': 0.88, 'Kansanga': 0.85,
        'Entebbe': 0.82
    },
    'Addis Ababa': {
        'Bole': 1.18, 'Old Airport (Kazanchis)': 1.12, 'CMC / Summit': 0.88,
        'Sarbet': 0.82, 'Piazza': 0.92, 'Arat Kilo': 1.02,
        'Mexico Area': 0.88, 'Gerji': 0.85, 'Ayat': 0.78,
        'Lideta': 0.80, 'Megenagna': 0.82, 'Gotera': 0.85,
        'Saris': 0.78, 'Lebu': 0.75
    },
    'Dakar': {
        'Plateau': 1.15, 'Almadies': 1.22, 'Ngor': 1.08,
        'Ouakam': 0.85, 'Fann': 1.05, 'Mermoz': 1.02,
        'Point E': 1.08, 'Sacré-Cœur': 0.95, 'Liberté': 0.88,
        'HLM': 0.78, 'Yoff': 0.82, 'Médina': 0.75,
        'Parcelles Assainies': 0.72, 'Guédiawaye': 0.70
    },
    'Tunis': {
        'La Marsa': 1.15, 'Sidi Bou Said': 1.22, 'Les Berges du Lac': 1.12,
        'La Goulette': 0.85, 'Mutuelleville': 1.02, 'El Menzah': 0.95,
        'Ariana': 0.82, 'Carthage': 1.08, 'Gammarth': 1.10,
        'Ennasr': 0.85, 'El Manar': 0.88, 'Manouba': 0.75,
        'Ben Arous': 0.78, 'Soukra': 0.82
    },

    // -- Middle East / Caucasus (Group B) --
    'Tangier': {
        'Kasbah': 1.15, 'Ville Nouvelle': 1.05, 'Malabata': 0.92,
        'Cap Spartel': 0.85, 'Iberia': 0.88, 'Marshan': 1.02,
        'Boukhalef': 0.78, 'Moghogha': 0.80, 'Beni Makada': 0.72,
        'Souani': 0.82, 'Tanja Balia': 0.92, 'Mdiq': 0.85,
        'Martil': 0.82
    },
    'Amman': {
        'Abdoun': 1.22, 'Jabal Amman': 1.12, 'Sweifieh': 1.08,
        'Tabarbour': 0.78, 'Jabal al-Hussein': 0.82, 'Shmeisani': 1.05,
        'Jabal al-Weibdeh': 1.02, 'Khalda': 0.95, 'Tla al-Ali': 0.92,
        'Marj al-Hamam': 0.78, 'Dabouq': 1.08, 'Abu Alanda': 0.75,
        'Jabal al-Nuzha': 0.80, 'Um Uthaina': 1.05
    },
    'Beirut': {
        'Achrafieh': 1.22, 'Hamra': 1.08, 'Mar Mikhael': 1.12,
        'Verdun': 1.05, 'Raouche': 0.92, 'Badaro': 1.02,
        'Clemenceau': 1.05, 'Saifi Village': 1.15, 'Ain el-Mraiseh': 1.10,
        'Tariq el-Jdideh': 0.78, 'Borj Hammoud': 0.75, 'Dekwaneh': 0.80,
        'Jounieh': 0.85, 'Antelias': 0.82, 'Baabda': 0.82
    },
    'Muscat': {
        'Qurum': 1.15, 'Al Mouj': 1.25, 'Mutrah': 1.05,
        'Al Khuwair': 0.92, 'Shatti Al Qurum': 1.18, 'Bawshar': 0.88,
        'Al Ghubra': 0.85, 'Madinat Sultan Qaboos': 1.02, 'Ruwi': 0.82,
        'Al Amarat': 0.78, 'Seeb': 0.82, 'Al Hail': 0.80,
        'Azaiba': 0.88
    },
    'Batumi': {
        'Old Town': 1.10, 'New Boulevard': 1.15, 'Makhinjauri': 0.82,
        'Gonio': 0.85, 'Aghmashenebeli': 0.92, 'Javakhishvili': 0.88,
        'Rustaveli': 1.02, 'Khelvachauri': 0.78, 'Sarpi': 0.75,
        'Chakvi': 0.78, 'Kobuléti': 0.72, 'Green Cape': 0.82
    },
    'Yerevan': {
        'Kentron (Center)': 1.15, 'Arabkir': 0.92, 'Davtashen': 0.85,
        'Avan': 0.78, 'Nor Nork': 0.82, 'Malatia-Sebastia': 0.78,
        'Shengavit': 0.80, 'Erebuni': 0.82, 'Nork-Marash': 0.88,
        'Kanaker-Zeytun': 0.82, 'Ajapnyak': 0.78, 'Nubarashen': 0.72
    },

    // -- Southeast Asia misc (Group B remaining) --
    'Luang Prabang': {
        'Old Town Peninsula': 1.15, 'Ban Xieng Mouane': 0.92, 'Ban Phonheuang': 0.82,
        'Ban Phanom': 0.78, 'Ban Xiengleck': 0.85, 'Ban Choumkhong': 0.80,
        'Ban Khoy': 0.78, 'Ban Pakham': 0.75, 'Ban Mano': 0.72,
        'Ban Naviengkham': 0.80
    },
    'Vientiane': {
        'Chanthabouly': 1.12, 'Sikhottabong': 0.92, 'Sisattanak': 1.05,
        'Naxaythong': 0.78, 'Xaysetha': 0.88, 'Hadxaifong': 0.80,
        'Saysettha': 0.85, 'That Luang': 0.92, 'Don Chan': 1.02,
        'Ban Anou': 0.88, 'Phonsinuan': 0.82, 'Thadeua Road': 0.85
    },
    'Yangon': {
        'Downtown': 1.12, 'Bahan': 1.18, 'Hlaing': 1.05,
        'Insein': 0.78, 'Kamaryut': 1.02, 'Sanchaung': 0.95,
        'Tamwe': 0.88, 'Mingalar Taungnyunt': 0.82, 'Mayangone': 0.88,
        'Dagon Myothit': 0.75, 'Yankin': 0.85, 'Thingangyun': 0.78,
        'Pazundaung': 0.82, 'Latha (Chinatown)': 0.88
    },
};
