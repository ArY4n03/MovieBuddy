import streamlit as st
from themoviedb import TMDb
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
api_key = os.getenv("TMDB_API_KEY")

tmdb = TMDb(key=api_key, language="en", region="IN")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction=''' You will be given some data and based on that you have to guess the movie name
  always give your response in a list form, and only give movie names and add a new line character after every movie name
'''
)

chat_session = model.start_chat(
  history=[
  ]
)
def search_movie(name):
    movies = tmdb.search().movies(name)

    if len(movies) > 0:

        col1,col2 = st.columns(2)
        movie_id = movies[0].id  
        movie = tmdb.movie(movie_id).details(append_to_response="credits,external_ids,images,videos")
        with col1:
            try:
                st.write(movie.title,movie.year)
                st.image(f"{movie.poster_url()}",width=400)
            except:
                st.warning('Error While getting Poster url')
        with col2:
            try:
                st.page_link(movie.imdb_url,label="IMDB Page", icon=None, help=None, disabled=False, use_container_width=None)
                st.page_link(movie.backdrop_url(), label="Backdrop Image", icon=None, help=None, disabled=False, use_container_width=None)
            except:
                st.warning("Error while loading IMDB links")
            if movie.adult:
                st.info("18+ Movie")
            else:
                st.info("Not a 18+ Movie")
                
            st.html("Genres :")
            for genre in movie.genres:
                st.write(genre.name)
            
        st.html("<hr>")

if "ask_ai" not in st.session_state:
    st.session_state.ask_ai = False

def ask():
    st.session_state.ask_ai = True

prompt = st.text_input('Enter anything about you movie')
ask_btn = st.button("Ask",on_click=ask)

if st.session_state.ask_ai:
    response = chat_session.send_message(prompt)
    movies = response.text.split("\n")
    for i in range(0,len(movies)-1): #not including last element as it is just "\n" (a newline character) 
        search_movie(movies[i])

    st.session_state.ask_ai = False

