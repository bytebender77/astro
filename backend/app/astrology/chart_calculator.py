"""
Vedic Astrology Chart Calculator
Uses Swiss Ephemeris for accurate planetary calculations
"""

import swisseph as swe
from datetime import datetime
from typing import Dict, List
from dateutil import tz


class VedicChartCalculator:
    """Calculate Vedic astrology birth charts using Swiss Ephemeris"""
    
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,
        'Ketu': swe.MEAN_NODE,
    }
    
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    HOUSES = [
        '1st House (Lagna/Self)', '2nd House (Wealth)', '3rd House (Courage)',
        '4th House (Mother/Home)', '5th House (Children)', '6th House (Enemies)',
        '7th House (Marriage)', '8th House (Longevity)', '9th House (Fortune)',
        '10th House (Career)', '11th House (Gains)', '12th House (Loss/Liberation)'
    ]
    
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    def __init__(self):
        """Initialize the calculator"""
        swe.set_ephe_path('')
        print("🔮 VedicChartCalculator initialized")
    
    def calculate_chart(self, date, time, latitude, longitude, timezone):
        """
        Calculate complete Vedic birth chart
        
        Args:
            date: Birth date (YYYY-MM-DD)
            time: Birth time (HH:MM)
            latitude: Birth place latitude
            longitude: Birth place longitude
            timezone: Timezone string
        
        Returns:
            Dictionary containing complete chart data
        """
        # Parse datetime
        dt_str = f"{date} {time}"
        local_tz = tz.gettz(timezone)
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        dt_local = dt_local.replace(tzinfo=local_tz)
        dt_utc = dt_local.astimezone(tz.UTC)
        
        # Calculate Julian day
        jd = swe.julday(
            dt_utc.year, dt_utc.month, dt_utc.day,
            dt_utc.hour + dt_utc.minute/60.0
        )
        
        # Calculate Ayanamsa (Lahiri)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa(jd)
        
        # Calculate planetary positions
        planets = self._calculate_planets(jd, ayanamsa)
        
        # Calculate Ascendant
        ascendant = self._calculate_ascendant(jd, latitude, longitude, ayanamsa)
        
        # Calculate houses
        houses = self._calculate_houses(ascendant)
        
        # Calculate Moon's Nakshatra
        moon_nakshatra = self._calculate_nakshatra(planets['Moon']['longitude'])
        
        # Determine planetary strengths
        strengths = self._calculate_strengths(planets, ascendant)
        
        # Generate basic interpretation
        interpretation = self._generate_basic_interpretation(
            planets, ascendant, moon_nakshatra
        )
        
        return {
            'birth_details': {
                'date': date,
                'time': time,
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'timezone': timezone
                },
                'ayanamsa': round(ayanamsa, 2)
            },
            'ascendant': ascendant,
            'planets': planets,
            'houses': houses,
            'moon_nakshatra': moon_nakshatra,
            'strengths': strengths,
            'interpretation': interpretation
        }
    
    def _calculate_planets(self, jd, ayanamsa):
        """Calculate positions of all planets"""
        planet_data = {}
        
        for name, planet_id in self.PLANETS.items():
            # Calculate planet position
            result = swe.calc_ut(jd, planet_id)
            tropical_long = result[0][0]
            
            # Convert to sidereal (Vedic)
            sidereal_long = tropical_long - ayanamsa
            
            # Normalize to 0-360
            if sidereal_long < 0:
                sidereal_long += 360
            
            # Special handling for Ketu (180° from Rahu)
            if name == 'Ketu':
                sidereal_long = (sidereal_long + 180) % 360
            
            # Determine sign and degree
            sign_num = int(sidereal_long / 30)
            degree_in_sign = sidereal_long % 30
            
            planet_data[name] = {
                'longitude': round(sidereal_long, 2),
                'sign': self.SIGNS[sign_num],
                'sign_num': sign_num,
                'degree': round(degree_in_sign, 2),
                'nakshatra': self.NAKSHATRAS[int(sidereal_long / 13.333333)],
                'house': None
            }
        
        return planet_data
    
    def _calculate_ascendant(self, jd, lat, lon, ayanamsa):
        """Calculate Ascendant (Lagna)"""
        # Calculate houses using Placidus system
        houses_result = swe.houses(jd, lat, lon)
        tropical_asc = houses_result[1][0]
        
        # Convert to sidereal
        sidereal_asc = tropical_asc - ayanamsa
        if sidereal_asc < 0:
            sidereal_asc += 360
        
        sign_num = int(sidereal_asc / 30)
        degree = sidereal_asc % 30
        
        return {
            'longitude': round(sidereal_asc, 2),
            'sign': self.SIGNS[sign_num],
            'sign_num': sign_num,
            'degree': round(degree, 2)
        }
    
    def _calculate_houses(self, ascendant):
        """Calculate house cusps"""
        houses = []
        asc_long = ascendant['longitude']
        
        for i in range(12):
            cusp_long = (asc_long + (i * 30)) % 360
            sign_num = int(cusp_long / 30)
            
            houses.append({
                'house': i + 1,
                'cusp_longitude': round(cusp_long, 2),
                'sign': self.SIGNS[sign_num],
                'description': self.HOUSES[i]
            })
        
        return houses
    
    def _calculate_nakshatra(self, longitude):
        """Calculate Nakshatra from longitude"""
        nakshatra_num = int(longitude / 13.333333)
        pada = int((longitude % 13.333333) / 3.333333) + 1
        
        return {
            'name': self.NAKSHATRAS[nakshatra_num],
            'pada': pada,
            'lord': self._get_nakshatra_lord(nakshatra_num)
        }
    
    def _get_nakshatra_lord(self, nakshatra_num):
        """Get ruling planet of Nakshatra"""
        lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
                'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        return lords[nakshatra_num % 9]
    
    def _calculate_strengths(self, planets, ascendant):
        """Calculate basic planetary strengths"""
        strengths = {}
        
        # Exaltation points
        exaltation = {
            'Sun': 10, 'Moon': 33, 'Mars': 298, 'Mercury': 165,
            'Jupiter': 95, 'Venus': 357, 'Saturn': 200
        }
        
        debilitation = {
            'Sun': 190, 'Moon': 213, 'Mars': 118, 'Mercury': 345,
            'Jupiter': 275, 'Venus': 177, 'Saturn': 20
        }
        
        for planet, data in planets.items():
            if planet in ['Rahu', 'Ketu']:
                continue
            
            long = data['longitude']
            strength_score = 50
            
            # Check exaltation
            if planet in exaltation:
                diff = abs(long - exaltation[planet])
                if diff < 15:
                    strength_score += (15 - diff) * 2
            
            # Check debilitation
            if planet in debilitation:
                diff = abs(long - debilitation[planet])
                if diff < 15:
                    strength_score -= (15 - diff) * 2
            
            strengths[planet] = {
                'score': max(0, min(100, strength_score)),
                'status': 'Strong' if strength_score > 70 else 'Moderate' if strength_score > 40 else 'Weak'
            }
        
        return strengths
    
    def _generate_basic_interpretation(self, planets, ascendant, moon_nakshatra):
        """Generate basic chart interpretation"""
        return {
            'ascendant_sign': f"Your rising sign (Lagna) is {ascendant['sign']}, which shapes your outward personality and life approach.",
            'moon_sign': f"Your Moon is in {planets['Moon']['sign']}, influencing your emotional nature and mind.",
            'moon_nakshatra': f"Your birth Nakshatra is {moon_nakshatra['name']} (Pada {moon_nakshatra['pada']}), ruled by {moon_nakshatra['lord']}.",
            'sun_sign': f"Your Sun is in {planets['Sun']['sign']}, representing your soul and core identity."
        }