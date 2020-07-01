const IdToCommodity = {
    01: "Animals; live",
    02: "Meat and edible meat offal",
    03: "Fish and crustaceans, molluscs and other aquatic invertebrates",
    04: "Dairy produce; birds eggs; natural honey; edible products of animal origin, not elsewhere specified or included",
    05: "Animal originated products; not elsewhere specified or included",
    06: "Trees and other plants, live; bulbs, roots and the like; cut flowers and ornamental foliage",
    07: "Vegetables and certain roots and tubers; edible",
    08: "Fruit and nuts, edible; peel of citrus fruit or melons",
    09: "Coffee, tea, mate and spices",
    10: "Cereals",
    11: "Products of the milling industry; malt, starches, inulin, wheat gluten",
    12: "Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit, industrial or medicinal plants; straw and fodder",
    13: "Lac; gums, resins and other vegetable saps and extracts",
    14: "Vegetable plaiting materials; vegetable products not elsewhere specified or included",
    15: "Animal or vegetable fats and oils and their cleavage products; prepared animal fats; animal or vegetable waxes",
    16: "Meat, fish or crustaceans, molluscs or other aquatic invertebrates; preparations thereof",
    17: "Sugars and sugar confectionery",
    18: "Cocoa and cocoa preparations",
    19: "Preparations of cereals, flour, starch or milk; pastrycooks products",
    20: "Preparations of vegetables, fruit, nuts or other parts of plants",
    21: "Miscellaneous edible preparations",
    22: "Beverages, spirits and vinegar",
    23: "Food industries, residues and wastes thereof; prepared animal fodder",
    24: "Tobacco and manufactured tobacco substitutes",
    25: "Salt; sulphur; earths, stone; plastering materials, lime and cement",
    26: "Ores, slag and ash",
    27: "Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes",
    28: "Inorganic chemicals; organic and inorganic compounds of precious metals; of rare earth metals, of radio-active elements and of isotopes",
    29: "Organic chemicals",
    30: "Pharmaceutical products",
    31: "Fertilizers",
    32: "Tanning or dyeing extracts; tannins and their derivatives; dyes, pigments and other colouring matter; paints, varnishes; putty, other mastics; inks",
    33: "Essential oils and resinoids; perfumery, cosmetic or toilet preparations",
    34: "Soap, organic surface-active agents; washing, lubricating, polishing or scouring preparations; artificial or prepared waxes, candles and similar articles, modelling pastes, dental waxes and dental preparations with a basis of plaster",
    35: "Albuminoidal substances; modified starches; glues; enzymes",
    36: "Explosives; pyrotechnic products; matches; pyrophoric alloys; certain combustible preparations",
    37: "Photographic or cinematographic goods",
    38: "Chemical products n.e.s.",
    39: "Plastics and articles thereof",
    40: "Rubber and articles thereof",
    41: "Raw hides and skins (other than furskins) and leather",
    42: "Articles of leather; saddlery and harness; travel goods, handbags and similar containers; articles of animal gut (other than silk-worm gut)",
    43: "Furskins and artificial fur; manufactures thereof",
    44: "Wood and articles of wood; wood charcoal",
    45: "Cork and articles of cork",
    46: "Manufactures of straw, esparto or other plaiting materials; basketware and wickerwork",
    47: "Pulp of wood or other fibrous cellulosic material; waste and scrap of paper or paperboard",
    48: "Paper and paperboard; articles of paper pulp, of paper or paperboard",
    49: "Printed books, newspapers, pictures and other products of the printing industry; manuscripts, typescripts and plans",
    50: "Silk",
    51: "Wool, fine or coarse animal hair; horsehair yarn and woven fabric",
    52: "Cotton",
    53: "Vegetable textile fibres; paper yarn and woven fabrics of paper yarn",
    54: "Man-made filaments; strip and the like of man-made textile materials",
    55: "Man-made staple fibres",
    56: "Wadding, felt and nonwovens, special yarns; twine, cordage, ropes and cables and articles thereof",
    57: "Carpets and other textile floor coverings",
    58: "Fabrics; special woven fabrics, tufted textile fabrics, lace, tapestries, trimmings, embroidery",
    59: "Textile fabrics; impregnated, coated, covered or laminated; textile articles of a kind suitable for industrial use",
    60: "Fabrics; knitted or crocheted",
    61: "Apparel and clothing accessories; knitted or crocheted",
    62: "Apparel and clothing accessories; not knitted or crocheted",
    63: "Textiles, made up articles; sets; worn clothing and worn textile articles; rags",
    64: "Footwear; gaiters and the like; parts of such articles",
    65: "Headgear and parts thereof",
    66: "Umbrellas, sun umbrellas, walking-sticks, seat sticks, whips, riding crops; and parts thereof",
    67: "Feathers and down, prepared; and articles made of feather or of down; artificial flowers; articles of human hair",
    68: "Stone, plaster, cement, asbestos, mica or similar materials; articles thereof",
    69: "Ceramic products",
    70: "Glass and glassware",
    71: "Natural, cultured pearls; precious, semi-precious stones; precious metals, metals clad with precious metal, and articles thereof; imitation jewellery; coin",
    72: "Iron and steel",
    73: "Iron or steel articles",
    74: "Copper and articles thereof",
    75: "Nickel and articles thereof",
    76: "Aluminium and articles thereof",
    78: "Lead and articles thereof",
    79: "Zinc and articles thereof",
    80: "Tin; articles thereof",
    81: "Metals; n.e.s., cermets and articles thereof",
    82: "Tools, implements, cutlery, spoons and forks, of base metal; parts thereof, of base metal",
    83: "Metal; miscellaneous products of base metal",
    84: "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof",
    85: "Electrical machinery and equipment and parts thereof; sound recorders and reproducers; television image and sound recorders and reproducers, parts and accessories of such articles",
    86: "Railway, tramway locomotives, rolling-stock and parts thereof; railway or tramway track fixtures and fittings and parts thereof; mechanical (including electro-mechanical) traffic signalling equipment of all kinds",
    87: "Vehicles; other than railway or tramway rolling stock, and parts and accessories thereof",
    88: "Aircraft, spacecraft and parts thereof",
    89: "Ships, boats and floating structures",
    90: "Optical, photographic, cinematographic, measuring, checking, medical or surgical instruments and apparatus; parts and accessories",
    91: "Clocks and watches and parts thereof",
    92: "Musical instruments; parts and accessories of such articles",
    93: "Arms and ammunition; parts and accessories thereof",
    94: "Furniture; bedding, mattresses, mattress supports, cushions and similar stuffed furnishings; lamps and lighting fittings, n.e.s.; illuminated signs, illuminated name-plates and the like; prefabricated buildings",
    95: "Toys, games and sports requisites; parts and accessories thereof",
    96: "Miscellaneous manufactured articles",
    97: "Works of art; collectors pieces and antiques",
    99: "Commodities not specified according to kind"
};


// Invert the map.
const CommodityToId = {};
Object.keys(IdToCommodity).forEach(key => { CommodityToId[IdToCommodity[key]] = key; });