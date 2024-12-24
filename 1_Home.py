from themoviedb import aioTMDb,TMDb
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
tmdb = TMDb(key=os.getenv("TMDB_API_KEY"), language="en", region="IN")


if "movie_name" not in st.session_state:
    st.session_state.movie_name = ""

if "movie_searched" not in st.session_state:
    st.session_state.movie_searched = False


class Main:

    def __init__(self):
        st.title("Movie Buddy")
        self.movie_name = st.text_input("Enter Movie Name")

        self.search = st.button("Search",on_click=self.searched, args=(self.movie_name,))

    def searched(self,movie_name): #this function will be called everytime search is pressed
        st.session_state.movie_name = movie_name
        st.session_state.movie_searched = True

    def search_movie(self,name):
        movies = tmdb.search().movies(name)
        st.html("<h1>Loading Movies</h1>")

        if len(movies) < 1:
            st.html("<h3> No matching results <h3>")
        
        for i in range(len(movies)):
            col1,col2 = st.columns(2)
            movie_id = movies[i].id  
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


if __name__ == "__main__":
    main = Main()
    if st.session_state.movie_searched:
        main.search_movie(st.session_state.movie_name)
        st.session_state.movie_searched = False

