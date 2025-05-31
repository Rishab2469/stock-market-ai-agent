import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys (set these in .env file)
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', '')

    # AI API Keys (Free APIs)
    # Get DeepSeek API key from: https://platform.deepseek.com/
    # DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')

    # Get Groq API key from: https://console.groq.com/
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

    # AI Analysis settings - Groq Only Configuration
    USE_AI_ANALYSIS = True  # Enable/disable AI analysis
    AI_TIMEOUT = 30  # Seconds to wait for AI response
    AI_FALLBACK_TO_RULES = True  # Use rule-based if AI fails
    PRIMARY_AI_MODEL = 'groq'  # Primary AI model to use (groq only)

    # Stock filtering parameters
    MIN_SENTIMENT_SCORE = 0.1  # Minimum positive sentiment for buy recommendation
    MIN_VOLUME_RATIO = 1.5     # Minimum volume compared to average
    MAX_PRICE_CHANGE = 0.05    # Maximum daily price change (5%)
    MIN_MARKET_CAP = 10000000000  # Minimum market cap (₹100 Cr in INR)

    # News analysis settings
    NEWS_LOOKBACK_DAYS = 7     # Days to look back for news
    MIN_NEWS_ARTICLES = 3      # Minimum articles needed for analysis

    # Indian Stock universe organized by TOP 10 industry sectors (up to 25 stocks per sector)
    STOCK_SECTORS = {
        'BANKING': [
            # Major Private Banks
            'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'INDUSINDBK.NS',
            # Public Sector Banks
            'SBIN.NS', 'PNB.NS', 'BANKBARODA.NS', 'CANBK.NS', 'UNIONBANK.NS',
            # Small Finance & Other Banks
            'FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'BANDHANBNK.NS', 'RBLBANK.NS', 'YESBANK.NS',
            # Regional Banks
            'SOUTHBANK.NS', 'IOB.NS', 'INDIANB.NS', 'CENTRALBK.NS', 'MAHABANK.NS',
            # Development Banks
            'IRFC.NS', 'RECLTD.NS', 'PFC.NS', 'HUDCO.NS', 'NABARD.NS'
        ],

        'INFORMATION_TECHNOLOGY': [
            # Large Cap IT
            'TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS',
            # Mid Cap IT Services
            'LTI.NS', 'MINDTREE.NS', 'MPHASIS.NS', 'LTTS.NS', 'COFORGE.NS',
            # Product Companies
            'PERSISTENT.NS', 'SONATSOFTW.NS', 'CYIENT.NS', 'ZENSAR.NS', 'HEXAWARE.NS',
            # Emerging IT
            'RAMPGREEN.NS', 'INTELLECT.NS', 'KPITTECH.NS', 'NIITTECH.NS', 'POLYCAB.NS',
            # IT Infrastructure
            'TATAELXSI.NS', 'ECLERX.NS', 'NEWGEN.NS', 'BIRLASOFT.NS', 'MASTEK.NS'
        ],

        'ENERGY_OIL_GAS': [
            # Oil & Gas Giants
            'RELIANCE.NS', 'ONGC.NS', 'BPCL.NS', 'IOC.NS', 'HINDPETRO.NS',
            # Gas Companies
            'GAIL.NS', 'IGL.NS', 'MGL.NS', 'GSPL.NS', 'ATGL.NS',
            # Petrochemicals
            'ONGCPETRO.NS', 'MRPL.NS', 'CPCL.NS', 'NRL.NS', 'HPCL.NS',
            # Power Generation
            'NTPC.NS', 'POWERGRID.NS', 'NHPC.NS', 'SJVN.NS', 'THERMAX.NS',
            # Renewable Energy
            'ADANIGREEN.NS', 'TATAPOWER.NS', 'TORNTPOWER.NS', 'CESC.NS', 'JSHL.NS'
        ],

        'FMCG_CONSUMER': [
            # FMCG Giants
            'HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS', 'BRITANNIA.NS', 'DABUR.NS',
            # Food & Beverages
            'TATACONSUM.NS', 'MARICO.NS', 'GODREJCP.NS', 'EMAMILTD.NS', 'JYOTHYLAB.NS',
            # Personal Care
            'COLPAL.NS', 'PGHH.NS', 'GILLETTE.NS', 'VBL.NS', 'RADICO.NS',
            # Packaged Foods
            'VARUN.NS', 'BIKAJI.NS', 'DEVYANI.NS', 'JUBLFOOD.NS', 'WESTLIFE.NS',
            # Consumer Durables
            'WHIRLPOOL.NS', 'VOLTAS.NS', 'BLUESTAR.NS', 'AMBER.NS', 'CROMPTON.NS'
        ],

        'AUTOMOTIVE': [
            # Passenger Vehicles
            'MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'EICHERMOT.NS', 'ASHOKLEY.NS',
            # Two Wheelers
            'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'TVSMOTORS.NS', 'BAJAJHLDNG.NS', 'ESCORTS.NS',
            # Commercial Vehicles
            'BHARATFORG.NS', 'MOTHERSON.NS', 'BALKRISIND.NS', 'MRF.NS', 'APOLLOTYRE.NS',
            # Auto Components
            'BOSCHLTD.NS', 'EXIDEIND.NS', 'AMARAJABAT.NS', 'SUNDRMFAST.NS', 'BHARAT.NS',
            # Electric Vehicles
            'TATAMTRDVR.NS', 'MAHINDCIE.NS', 'TIINDIA.NS', 'MINDACORP.NS', 'SWARAJENG.NS'
        ],

        'PHARMACEUTICALS': [
            # Large Pharma
            'SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS', 'DIVISLAB.NS', 'BIOCON.NS',
            # Mid Cap Pharma
            'LUPIN.NS', 'AUROPHARMA.NS', 'TORNTPHARM.NS', 'CADILAHC.NS', 'GLENMARK.NS',
            # Specialty Pharma
            'ALKEM.NS', 'LALPATHLAB.NS', 'METROPOLIS.NS', 'THYROCARE.NS', 'KRBL.NS',
            # API & Formulations
            'DIVIS.NS', 'GRANULES.NS', 'STRIDES.NS', 'NATCOPHAR.NS', 'SUVEN.NS',
            # Healthcare Services
            'APOLLOHOSP.NS', 'FORTIS.NS', 'MAXHEALTH.NS', 'NARAYANA.NS', 'RAINBOW.NS'
        ],

        'FINANCE_NBFC': [
            # Large NBFCs
            'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'HDFCAMC.NS', 'SBICARD.NS', 'CHOLAFIN.NS',
            # Insurance
            'LICI.NS', 'SBILIFE.NS', 'HDFCLIFE.NS', 'ICICIPRULI.NS', 'MAXLIFE.NS',
            # Asset Management
            'RELCAPITAL.NS', 'IIFL.NS', 'MOTILALOFS.NS', 'ANGELONE.NS', 'CDSL.NS',
            # Housing Finance
            'LICHSGFIN.NS', 'CANFINHOME.NS', 'GRUH.NS', 'REPCO.NS', 'APTUS.NS',
            # Microfinance
            'SPANDANA.NS', 'CREDITACC.NS', 'UJJIVAN.NS', 'EQUITAS.NS', 'SURYODAY.NS'
        ],

        'METALS_MINING': [
            # Steel Companies
            'TATASTEEL.NS', 'JSWSTEEL.NS', 'SAIL.NS', 'JINDALSTEL.NS', 'NMDC.NS',
            # Aluminum & Copper
            'HINDALCO.NS', 'NALCO.NS', 'BALRAMCHIN.NS', 'HINDZINC.NS', 'VEDL.NS',
            # Coal & Mining
            'COALINDIA.NS', 'GMRINFRA.NS', 'ADANIENT.NS', 'WELCORP.NS', 'MOIL.NS',
            # Specialty Metals
            'RATNAMANI.NS', 'APL.NS', 'KALYANKJIL.NS', 'TIITAN.NS', 'MANAPPURAM.NS',
            # Metal Processing
            'JSWENERGY.NS', 'JSPL.NS', 'RSWM.NS', 'WELSPUNIND.NS', 'ORIENTREF.NS'
        ],

        'INFRASTRUCTURE': [
            # Construction Giants
            'LT.NS', 'ULTRACEMCO.NS', 'GRASIM.NS', 'SHREECEM.NS', 'ACC.NS',
            # Ports & Logistics
            'ADANIPORTS.NS', 'CONCOR.NS', 'ALLCARGO.NS', 'GATI.NS', 'TCI.NS',
            # Power Infrastructure
            'POWERGRID.NS', 'NTPC.NS', 'NHPC.NS', 'SJVN.NS', 'IRCON.NS',
            # Roads & Highways
            'IRB.NS', 'SADBHAV.NS', 'DILIPBUILDCON.NS', 'ASHOKA.NS', 'HCC.NS',
            # Real Estate
            'DLF.NS', 'GODREJPROP.NS', 'OBEROIRLTY.NS', 'PRESTIGE.NS', 'BRIGADE.NS'
        ],

        'CEMENT': [
            # Major Cement
            'ULTRACEMCO.NS', 'GRASIM.NS', 'SHREECEM.NS', 'AMBUJACEM.NS', 'ACC.NS',
            # Regional Cement
            'DALMIACEMT.NS', 'RAMCOCEM.NS', 'JKCEMENT.NS', 'HEIDELBERG.NS', 'PRISM.NS',
            # Building Materials
            'JKPAPER.NS', 'TNPL.NS', 'BALRAMCHIN.NS', 'ORIENTCEM.NS', 'INDIACEM.NS',
            # Construction Materials
            'CENTURYPLY.NS', 'GREENPLY.NS', 'ASTRAL.NS', 'SUPREME.NS', 'NILKAMAL.NS',
            # Infrastructure Materials
            'HEIDELBERG.NS', 'BIRLACEM.NS', 'MAGMA.NS', 'KESORAMIND.NS', 'BURNPUR.NS'
        ],

        'DEFENCE': [
            # Defence PSUs (Major Players)
            'HAL.NS', 'BEL.NS', 'BEML.NS', 'GRSE.NS', 'COCHINSHIP.NS',
            # Aerospace & Defence
            'MIDHANI.NS', 'ORDNFAC.NS', 'MAZAGON.NS', 'IRCON.NS', 'RVNL.NS',
            # Defence Electronics & Technology
            'DATAPATTNS.NS', 'ZENTEC.NS', 'RTNPOWER.NS', 'KECL.NS', 'RAILTEL.NS',
            # Shipbuilding & Marine
            'TIINDIA.NS', 'ABB.NS', 'THERMAX.NS', 'KIRLOSENG.NS', 'ELECON.NS',
            # Defence Equipment & Components
            'BHEL.NS', 'SAIL.NS', 'NMDC.NS', 'MOIL.NS', 'NATIONALUM.NS'
        ]
    }

    # Flatten all stocks into a single list for backward compatibility
    STOCK_SYMBOLS = []
    for sector, stocks in STOCK_SECTORS.items():
        STOCK_SYMBOLS.extend(stocks)

    # Remove duplicates while preserving order
    STOCK_SYMBOLS = list(dict.fromkeys(STOCK_SYMBOLS))

    # Risk management
    MAX_RECOMMENDATIONS = 11   # Maximum number of buy recommendations
    RISK_TOLERANCE = 'medium'  # low, medium, high

    # Web app settings
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
