import random
from pathlib import Path
from manim import *
from config import *
from common import CommonUtils

class TitleCard(Scene, CommonUtils):

    matrix_style = MatrixStyle()
    red_style = RedStyle()
    yellow_style = YellowStyle()
    blue_style = BlueStyle()
    purple_style = PurpleStyle()
    pink_style = PinkStyle()
    white_style = WhiteStyle()
    amber_style = AmberStyle()

    def construct(self):

        self.setup_scene()

        CHAR_WIDTH = 0.5 
        COLS = 40
        CLI_FONT = "Noto Sans Mono CJK JP" 
        KATAKANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        CHARS = KATAKANA + "0123456789"

        columns = VGroup()
        for x in range(COLS):
            col_length = random.randint(20, 30)
            column = VGroup()
            for y in range(col_length):
                char_opacity = 1.0 - (y / col_length)
                color = GHOST_WHITE if y == 0 else MATRIX_GREEN
                char = Text(random.choice(CHARS), font=CLI_FONT, font_size=18, color=color).set_opacity(max(char_opacity, 0.1))
                column.add(char)
            column.arrange(DOWN, buff=0.15)
            initial_x = (x - COLS/2) * CHAR_WIDTH
            column.move_to([initial_x, random.uniform(6, 15), 0])
            column.initial_x = initial_x
            column.fall_speed = random.uniform(4, 9)
            columns.add(column)

        def update_column(obj, dt):
            obj.shift(DOWN * obj.fall_speed * dt)
            for _ in range(2):
                if random.random() > 0.7:
                    idx = random.randint(0, len(obj) - 1)
                    old_char = obj[idx]
                    new_char = Text(random.choice(CHARS), font=CLI_FONT, font_size=18, color=old_char.get_color())
                    new_char.move_to(old_char.get_center())
                    new_char.set_opacity(old_char.get_opacity())
                    obj[idx].become(new_char)
            if obj.get_top()[1] < -6:
                obj.move_to([obj.initial_x, random.uniform(7, 14), 0])
                obj.fall_speed = random.uniform(4, 9)

        for col in columns:
            col.add_updater(update_column)
            
        self.add(columns)
        self.wait(5)

        self.intro_animation("NETWORK COMPONENTS & ARCHITECTURE","Access Granted !")

# 'Adwaita Mono', 'Adwaita Sans', 'Cantarell', 'Hack', 'Liberation Mono', 'Liberation       text_mobject.py:464
# Sans', 'Liberation Serif', 'Monospace', 'Noto Color Emoji', 'Noto Fangsong KSS Rotated', 'Noto Fangsong KSS                      
# Vertical', 'Noto Kufi Arabic', 'Noto Music', 'Noto Naskh Arabic', 'Noto Naskh Arabic UI', 'Noto Nastaliq                         
# Urdu', 'Noto Rashi Hebrew', 'Noto Sans', 'Noto Sans Adlam', 'Noto Sans Adlam Unjoined', 'Noto Sans Anatolian                     
# Hieroglyphs', 'Noto Sans Arabic', 'Noto Sans Arabic UI', 'Noto Sans Armenian', 'Noto Sans Avestan', 'Noto                        
# Sans Balinese', 'Noto Sans Bamum', 'Noto Sans Bassa Vah', 'Noto Sans Batak', 'Noto Sans Bengali', 'Noto Sans                     
# Bengali UI', 'Noto Sans Bhaiksuki', 'Noto Sans Brahmi', 'Noto Sans Buginese', 'Noto Sans Buhid', 'Noto Sans                      
# Canadian Aboriginal', 'Noto Sans Carian', 'Noto Sans Caucasian Albanian', 'Noto Sans Chakma', 'Noto Sans                         
# Cham', 'Noto Sans Cherokee', 'Noto Sans Chorasmian', 'Noto Sans Coptic', 'Noto Sans Cuneiform', 'Noto Sans                       
# Cypriot', 'Noto Sans Cypro Minoan', 'Noto Sans Deseret', 'Noto Sans Devanagari', 'Noto Sans Devanagari UI',                      
# 'Noto Sans Duployan', 'Noto Sans Egyptian Hieroglyphs', 'Noto Sans Elbasan', 'Noto Sans Elymaic', 'Noto Sans                     
# Ethiopic', 'Noto Sans Georgian', 'Noto Sans Glagolitic', 'Noto Sans Gothic', 'Noto Sans Grantha', 'Noto Sans                     
# Gujarati', 'Noto Sans Gujarati UI', 'Noto Sans Gunjala Gondi', 'Noto Sans Gurmukhi', 'Noto Sans Gurmukhi UI',                    
# 'Noto Sans Hanifi Rohingya', 'Noto Sans Hanunoo', 'Noto Sans Hatran', 'Noto Sans Hebrew', 'Noto Sans Imperial                    
# Aramaic', 'Noto Sans Indic Siyaq Numbers', 'Noto Sans Inscriptional Pahlavi', 'Noto Sans Inscriptional                           
# Parthian', 'Noto Sans Javanese', 'Noto Sans Kaithi', 'Noto Sans Kannada', 'Noto Sans Kannada UI', 'Noto Sans                     
# Kawi', 'Noto Sans Kayah Li', 'Noto Sans Kharoshthi', 'Noto Sans Khmer', 'Noto Sans Khojki', 'Noto Sans                           
# Khudawadi', 'Noto Sans Lao', 'Noto Sans Lao Looped', 'Noto Sans Lepcha', 'Noto Sans Limbu', 'Noto Sans Linear                    
# A', 'Noto Sans Linear B', 'Noto Sans Lisu', 'Noto Sans Lycian', 'Noto Sans Lydian', 'Noto Sans Mahajani',                        
# 'Noto Sans Malayalam', 'Noto Sans Malayalam UI', 'Noto Sans Mandaic', 'Noto Sans Manichaean', 'Noto Sans                         
# Marchen', 'Noto Sans Masaram Gondi', 'Noto Sans Math', 'Noto Sans Mayan Numerals', 'Noto Sans Medefaidrin',                      
# 'Noto Sans Meetei Mayek', 'Noto Sans Mende Kikakui', 'Noto Sans Meroitic', 'Noto Sans Miao', 'Noto Sans                          
# Modi', 'Noto Sans Mongolian', 'Noto Sans Mono', 'Noto Sans Mono CJK JP', 'Noto Sans Mro', 'Noto Sans                             
# Multani', 'Noto Sans Myanmar', 'Noto Sans NKo', 'Noto Sans NKo Unjoined', 'Noto Sans Nabataean', 'Noto Sans                      
# Nag Mundari', 'Noto Sans Nandinagari', 'Noto Sans New Tai Lue', 'Noto Sans Newa', 'Noto Sans Nushu', 'Noto                       
# Sans Ogham', 'Noto Sans Ol Chiki', 'Noto Sans Old Hungarian', 'Noto Sans Old Italic', 'Noto Sans Old North                       
# Arabian', 'Noto Sans Old Permic', 'Noto Sans Old Persian', 'Noto Sans Old Sogdian', 'Noto Sans Old South                         
# Arabian', 'Noto Sans Old Turkic', 'Noto Sans Oriya', 'Noto Sans Osage', 'Noto Sans Osmanya', 'Noto Sans                          
# Pahawh Hmong', 'Noto Sans Palmyrene', 'Noto Sans Pau Cin Hau', 'Noto Sans PhagsPa', 'Noto Sans Phoenician',                      
# 'Noto Sans Psalter Pahlavi', 'Noto Sans Rejang', 'Noto Sans Runic', 'Noto Sans Samaritan', 'Noto Sans                            
# Saurashtra', 'Noto Sans Sharada', 'Noto Sans Shavian', 'Noto Sans Siddham', 'Noto Sans SignWriting', 'Noto                       
# Sans Sinhala', 'Noto Sans Sinhala UI', 'Noto Sans Sogdian', 'Noto Sans Sora Sompeng', 'Noto Sans Soyombo',                       
# 'Noto Sans Sundanese', 'Noto Sans Sunuwar', 'Noto Sans Syloti Nagri', 'Noto Sans Symbols', 'Noto Sans Symbols                    
# 2', 'Noto Sans Syriac', 'Noto Sans Syriac Eastern', 'Noto Sans Syriac Western', 'Noto Sans Tagalog', 'Noto                       
# Sans Tagbanwa', 'Noto Sans Tai Le', 'Noto Sans Tai Tham', 'Noto Sans Tai Viet', 'Noto Sans Takri', 'Noto Sans                    
# Tamil', 'Noto Sans Tamil Supplement', 'Noto Sans Tamil UI', 'Noto Sans Tangsa', 'Noto Sans Telugu', 'Noto                        
# Sans Telugu UI', 'Noto Sans Test', 'Noto Sans Thaana', 'Noto Sans Thai', 'Noto Sans Thai Looped', 'Noto Sans                     
# Tifinagh', 'Noto Sans Tifinagh APT', 'Noto Sans Tifinagh Adrar', 'Noto Sans Tifinagh Agraw Imazighen', 'Noto                     
# Sans Tifinagh Ahaggar', 'Noto Sans Tifinagh Air', 'Noto Sans Tifinagh Azawagh', 'Noto Sans Tifinagh Ghat',                       
# 'Noto Sans Tifinagh Hawad', 'Noto Sans Tifinagh Rhissa Ixa', 'Noto Sans Tifinagh SIL', 'Noto Sans Tifinagh                       
# Tawellemmet', 'Noto Sans Tirhuta', 'Noto Sans Ugaritic', 'Noto Sans Vai', 'Noto Sans Vithkuqi', 'Noto Sans                       
# Wancho', 'Noto Sans Warang Citi', 'Noto Sans Yi', 'Noto Sans Zanabazar Square', 'Noto Serif', 'Noto Serif                        
# Ahom', 'Noto Serif Armenian', 'Noto Serif Balinese', 'Noto Serif Bengali', 'Noto Serif Devanagari', 'Noto                        
# Serif Display', 'Noto Serif Dives Akuru', 'Noto Serif Dogra', 'Noto Serif Ethiopic', 'Noto Serif Georgian',                      
# 'Noto Serif Grantha', 'Noto Serif Gujarati', 'Noto Serif Gurmukhi', 'Noto Serif Hebrew', 'Noto Serif                             
# Hentaigana', 'Noto Serif Kannada', 'Noto Serif Khitan Small Script', 'Noto Serif Khmer', 'Noto Serif Khojki',                    
# 'Noto Serif Lao', 'Noto Serif Makasar', 'Noto Serif Malayalam', 'Noto Serif Myanmar', 'Noto Serif NP Hmong',                     
# 'Noto Serif Old Uyghur', 'Noto Serif Oriya', 'Noto Serif Ottoman Siyaq', 'Noto Serif Sinhala', 'Noto Serif                       
# Tamil', 'Noto Serif Tangut', 'Noto Serif Telugu', 'Noto Serif Test', 'Noto Serif Thai', 'Noto Serif Tibetan',                    
# 'Noto Serif Todhri', 'Noto Serif Toto', 'Noto Serif Vithkuqi', 'Noto Serif Yezidi', 'Noto Traditional Nushu',                    
# 'Noto Znamenny Musical Notation', 'Sans', 'Serif', 'Source Code Pro', 'SourceCodeVF', 'System-ui'