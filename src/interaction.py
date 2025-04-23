from datetime import datetime,date

def mood_Mapping(emotion):
    if emotion=="happy" :
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0
    
    if emotion=="sadness":
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0
        print("yes")
    
    if emotion=="angry":
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0

    if emotion=="fearful":
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0

    if emotion=="romantic":
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0
    
    if emotion=="excited":
       valence=0
       energy=0
       danceability=0
       tempo=0
       mode=1
       acousticness=0
       instrumentalness=0
    
    if emotion=="sadness":
        valence=0
        energy=0
        danceability=0
        tempo=0
        mode=1
        acousticness=0
        instrumentalness=0

    v=[ valence,energy,danceability,tempo,mode,acousticness,instrumentalness]
    return v

def generate_playlist(emotion):
    today = date.today()
    print("Today's date:", today)

    day = today.strftime("%m/%d/%y")
    print("Current date =",day)
    playlist_name=emotion.capitalize()+'-'+day

    #get mood mapping parameters
    #send request to make playlist
    #return playlist_name for logs on GUI 
    # 

    return playlist_name   
