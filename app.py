import streamlit as st
import base64


# ==============================
# DARK OIL CALCULATION
# ==============================

def calculate_dark_oil(cities):

    production = {
        1: 100,
        2: 200,
        3: 300,
        4: 400,
        5: 500,
        6: 600
    }

    total = 0

    for level in cities:
        total += cities[level] * production[level]

    return total



# ==============================
# CITY OPEN DAYS
# ==============================

city_open_days = {
    1: "Level 1 City Opens",
    5: "Level 2 City Opens",
    8: "Level 3 City Opens",
    12: "Level 4 City Opens",
    15: "Level 5 City Opens",
    19: "Level 6 City Opens"
}



# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="⚫ X-Clash Dark Oil Simulator - Animality",
    page_icon="⚫"
)



# ==============================
# X-CLASH GAME PANEL BACKGROUND
# ==============================

def add_bg(image_file):

    with open(image_file, "rb") as file:

        encoded = base64.b64encode(
            file.read()
        ).decode()


    st.markdown(
        f"""
        <style>

        .stApp {{

            background-color: #111111;

        }}


        .block-container {{

            background-image:
            linear-gradient(
                rgba(0,0,0,0.65),
                rgba(0,0,0,0.65)
            ),
            url("data:image/jpg;base64,{encoded}");

            background-size: 800px 800px;

            background-repeat: no-repeat;

            background-position: center top;

            padding: 40px;

            border-radius: 20px;

        }}

        </style>
        """,
        unsafe_allow_html=True
    )


add_bg("background.jpg")


# ==============================
# TITLE
# ==============================

st.markdown(
    """
    <h1 style="
        text-align:center;
        color:#9b59ff;
        font-size:42px;
        ">
        ⚫ X-Clash Dark Oil Simulator ⚫<br>
        <span style="font-size:32px;">
        - Animality -
        </span>
    </h1>
    """,
    unsafe_allow_html=True
)


st.write(
    "Calculate your Dark Oil production throughout the City Race."
)



# ==============================
# SESSION STORAGE
# ==============================

if "day" not in st.session_state:
    st.session_state.day = 1

if "part" not in st.session_state:
    st.session_state.part = 1

if "total_oil" not in st.session_state:
    st.session_state.total_oil = 0

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "last_result" not in st.session_state:
    st.session_state.last_result = {}

if "finished" not in st.session_state:
    st.session_state.finished = False



# ==============================
# RESET
# ==============================

if st.button("🔄 Reset Simulation"):

    st.session_state.day = 1
    st.session_state.part = 1
    st.session_state.total_oil = 0
    st.session_state.calculated = False
    st.session_state.last_result = {}
    st.session_state.finished = False

    st.rerun()



# ==============================
# FINISHED
# ==============================

if st.session_state.finished:

    st.success("Simulation Finished!")

    st.subheader("Final Results")

    st.write(
        f"⚫ Final Dark Oil: **{st.session_state.total_oil:,}**"
    )

    st.stop()



# ==============================
# TIMELINE DISPLAY
# ==============================

day = st.session_state.day


if day in city_open_days:

    st.header(
        f"Day {day} ({city_open_days[day]})"
    )


    st.info(
        f"Day {day} Part {st.session_state.part} - 12 hours"
    )


    hours_default = 12

    total_parts = 2


else:

    st.header(
        f"Day {day}"
    )


    st.info(
        f"Day {day} - 24 hours"
    )


    hours_default = 24

    total_parts = 1



# ==============================
# CURRENT DARK OIL
# ==============================

st.divider()

st.subheader(
    f"⚫ Current Dark Oil: {st.session_state.total_oil:,}"
)



# ==============================
# CITY INPUT
# ==============================

st.subheader("Owned Cities")


cities = {}


for level in range(1, 7):

    cities[level] = st.number_input(
        f"Level {level} Cities",
        min_value=0,
        value=0,
        step=1,
        key=f"level_{level}"
    )



hours = st.number_input(
    "Hours Passed",
    min_value=1,
    value=hours_default,
    step=1
)



# ==============================
# CALCULATE
# ==============================

if st.button("⚫ Calculate Dark Oil"):


    dark_oil_per_hour = calculate_dark_oil(cities)


    earned = dark_oil_per_hour * hours


    st.session_state.total_oil += earned


    st.session_state.last_result = {

        "production": dark_oil_per_hour,

        "hours": hours,

        "earned": earned,

        "total": st.session_state.total_oil

    }


    st.session_state.calculated = True




# ==============================
# RESULTS
# ==============================

if st.session_state.calculated:

    result = st.session_state.last_result


    st.divider()


    st.subheader(
        "============== RESULTS =============="
    )


    st.write(
        f"⚫ Dark Oil / Hour : **{result['production']:,}**"
    )


    st.write(
        f"⏱️ Hours Passed : **{result['hours']}**"
    )


    st.write(
        f"⚫ Dark Oil Earned : **{result['earned']:,}**"
    )


    st.write(
        f"📦 Current Total : **{result['total']:,}**"
    )


    st.divider()



    # ==============================
    # CONTINUE
    # ==============================

    if st.button("Continue ➡️"):


        if total_parts == 2:

            if st.session_state.part == 1:

                st.session_state.part = 2

            else:

                st.session_state.day += 1
                st.session_state.part = 1


        else:

            st.session_state.day += 1



        if st.session_state.day > 19:

            st.session_state.finished = True



        st.session_state.calculated = False


        st.rerun()
