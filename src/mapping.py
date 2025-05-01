"""high >=0.6; 0.3<=mid<0.6; low<0.3"""

#Mapping based on distillRoberTA text emotion_classifier
def map_song_to_emotion(arousal, valence,danceability,loudness,acousticness,instrumentalness):
  loudness_min = -60  # typical quietest
  loudness_max = 0    # digital ceiling
  normalized_loudness=(loudness-loudness_min)/(loudness_max-loudness_min)

  # Differentiate Anger and Fear if in ambiguous zone
  if valence < 0.35 and arousal > 0.65:
    if danceability > 0.5 and normalized_loudness > 0.7:
      return "anger"
    elif acousticness > 0.4 or instrumentalness > 0.6:
      return "fear"
    else:
      return "anger"  #fallback

  if valence > 0.65 and arousal > 0.65:
    return "joy"
  elif valence < 0.35 and arousal < 0.4:
    return "sadness"
  elif valence < 0.35 and 0.4 <= arousal <= 0.65:
    return "disgust"
  elif 0.35 <= valence <= 0.65 and arousal > 0.65:
    return "surprise"
  elif 0.35 <= valence <= 0.65 and 0.4 <= arousal <= 0.65:
    return "neutral"
  elif valence > 0.65 and 0.4 <= arousal <= 0.65:
    return "joy"  # Still positive but calmer
  else:
    return "neutral"

def map_emotion_to_song_characteristics(emotion):
  loudness_min = -60  # typical quietest
  loudness_max = 0    # digital ceiling
  
  if emotion=="anger":
    min_valence=0
    max_valence=0.35 
    min_arousal=0.65
    max_arousal=1
    min_danceability=0.5
    max_danceability=1
    min_loudness=0,7*(loudness_max-loudness_min)+loudness_min
    max_loudness=loudness_max
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal,min_danceability,max_danceability,min_loudness,max_loudness]
   
  if emotion=="fear":
    min_valence=0
    max_valence=0.35 
    min_arousal=0.65
    max_arousal=1
    min_acousticness=0.4 
    max_acousticness=1
    min_instrumentalness=0.6
    max_instrumentalness=1
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal,min_acousticness,max_acousticness,min_instrumentalness,max_instrumentalness]
    
  if emotion=="joy":
    min_valence=0.65 
    max_valence=1
    min_arousal=0.5
    max_arousal= 1
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal]
 
  if emotion=="sadness":
    min_valence=0
    max_valence=0.35
    min_arousal=0
    max_arousal= 0.4
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal]
  
  if emotion=="surprise":
    min_valence=0.35 
    max_valence= 0.65 
    min_arousal=0.65
    max_arousal=1
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal]
  
  if emotion=="disgust":
    min_valence=0
    max_valence=0.35
    min_arousal=0.4 
    max_arousal= 0.65
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal]
    
  if emotion=="neutral":
    min_valence=0.35
    max_valence=0.65
    min_arousal=0.4 
    max_arousal= 0.65
    characteristics=[emotion,min_valence,max_valence,min_arousal,max_arousal]
  
  return characteristics
    
def compute_arousal(energy,tempo,loudness,danceability,speechiness,liveness,acousticness):
  loudness_min = -60  # typical quietest
  loudness_max = 0    # digital ceiling
  tempo_min = 40
  tempo_max = 230

  normalized_tempo=(tempo-tempo_min)/(tempo_max-tempo_min)
  normalized_loudness=(loudness-loudness_min)/(loudness_max-loudness_min)

  arousal_raw_max=1.094176
  arousal_raw_min=0

  #max arousal :1.094176
  #min arousal :0.0

  arousal_raw = 0.599082 * energy + 0.205437 * normalized_tempo + 0.546612 * normalized_loudness + 0.077367 * danceability + 0.081076 * speechiness +0.109535 * liveness -0.524933 * acousticness
  normalized_arousal=(arousal_raw-arousal_raw_min)/(arousal_raw_max-arousal_raw_min)

  if 0<=normalized_arousal and normalized_arousal<=1:
    return normalized_arousal
  return energy

def detect_song_emotion(energy,tempo,loudness,danceability,speechiness,liveness,acousticness, valence,instrumentalness):
  arousal=compute_arousal(energy,tempo,loudness,danceability,speechiness,liveness,acousticness)
  return map_song_to_emotion(arousal, valence,danceability,loudness,acousticness,instrumentalness)

def map_seed_genres_to_emotion(emotion):
  emotion_genre_map = {
    'anger': ['metal', 'heavy-metal', 'metalcore', 'death-metal', 'black-metal',
              'hardcore', 'hard-rock', 'punk', 'punk-rock', 'grindcore', 'industrial', 'hardstyle', 'emo'],
    
    'fear': ['minimal-techno', 'ambient', 'industrial', 'trip-hop', 'black-metal',
             'grindcore', 'soundtracks', 'goth'],
    
    'joy': ['pop', 'dance', 'edm', 'house', 'disco', 'funk', 'electro', 'latino',
            'samba', 'salsa', 'reggae', 'reggaeton', 'k-pop', 'j-pop', 'summer', 'happy', 'party', 'brazil'],
    
    'sadness': ['acoustic', 'singer-songwriter', 'indie', 'indie-pop', 'blues', 'classical',
                'ambient', 'sad', 'piano', 'folk', 'emo', 'rainy-day'],
    
    'disgust': ['grindcore', 'death-metal', 'hardcore', 'black-metal', 'industrial'],
    
    'surprise': ['jazz', 'progressive-house', 'psych-rock', 'trance', 'techno',
                 'alternative', 'experimental', 'soundtracks', 'anime'],
    
    'neutral': ['chill', 'ambient', 'classical', 'deep-house', 'minimal-techno',
                'study', 'sleep', 'new-age', 'world-music', 'bossanova']
  }
  return emotion_genre_map[emotion]









"""def main():
  print(f"max arousal :{compute_arousal(1,230,0,1,1,1,1)}")
  print(f"min arousal :{compute_arousal(0,40,-60,0,0,0,0)}")"""

