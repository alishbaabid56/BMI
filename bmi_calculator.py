import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_bmi(weight, height):
    """Calculate BMI and return value and category"""
    try:
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal Weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        return round(bmi, 1), category
    except ZeroDivisionError:
        return None, "Error: Height cannot be zero"

def create_bmi_chart(bmi):
    """Create a visual representation of BMI"""
    fig, ax = plt.subplots(figsize=(10, 1))
    sns.barplot(x=[i for i in range(15, 41)], y=[0.1] * 26, color='lightgray', ax=ax)
    
    ax.axvspan(15, 18.5, alpha=0.3, color='blue', label='Underweight')
    ax.axvspan(18.5, 25, alpha=0.3, color='green', label='Normal')
    ax.axvspan(25, 30, alpha=0.3, color='yellow', label='Overweight')
    ax.axvspan(30, 40, alpha=0.3, color='red', label='Obese')
    
    if bmi:
        ax.axvline(x=bmi, color='black', linestyle='--', label=f'Your BMI ({bmi})')
    
    ax.set_ylim(0, 0.2)
    ax.set_yticks([])
    ax.set_xlabel("BMI")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=5)
    return fig

def main():
    st.set_page_config(page_title="Enhanced BMI Calculator", page_icon="🏋️‍♂️", layout="wide")

    # Initialize session state
    if 'bmi_history' not in st.session_state:
        st.session_state.bmi_history = []

    st.title("Enhanced BMI Calculator")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.write("This app calculates your BMI and tracks your history.")
        if st.button("Clear History"):
            st.session_state.bmi_history = []
            st.success("History cleared!")

    # Main layout
    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form(key='bmi_form'):
            unit_system = st.radio("Unit System:", ("Metric (kg, m)", "Imperial (lb, ft)"))
            
            if unit_system == "Metric (kg, m)":
                weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
                height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.7, step=0.01)
            else:
                weight = st.number_input("Weight (lb)", min_value=40.0, max_value=650.0, value=150.0, step=0.1)
                height = st.number_input("Height (ft)", min_value=2.0, max_value=9.0, value=5.5, step=0.1)

            col_submit, col_reset = st.columns(2)
            with col_submit:
                submit = st.form_submit_button("Calculate BMI")
            with col_reset:
                reset = st.form_submit_button("Reset")

        # Handle form submission
        if submit:
            if unit_system == "Imperial (lb, ft)":
                weight = weight * 0.453592  # lb to kg
                height = height * 0.3048    # ft to m

            bmi, category = calculate_bmi(weight, height)
            if bmi:
                st.success(f"Your BMI: **{bmi}** | Category: **{category}**")
                st.session_state.bmi_history.append({'BMI': bmi, 'Category': category})
            else:
                st.error(category)

        if reset:
            st.rerun()  

      
        if st.session_state.bmi_history:
            st.pyplot(create_bmi_chart(st.session_state.bmi_history[-1]['BMI']))
        else:
            st.pyplot(create_bmi_chart(None))

    with col2:
        st.subheader("BMI History")
        if st.session_state.bmi_history:
            df = pd.DataFrame(st.session_state.bmi_history)
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No calculations yet")

        st.subheader("BMI Categories")
        st.markdown("""
        - Underweight: < 18.5 (Blue)
        - Normal: 18.5 - 24.9 (Green)
        - Overweight: 25 - 29.9 (Yellow)
        - Obese: ≥ 30 (Red)
        """)

    # Footer
    st.markdown(
        """
        <style>
        .footer {position: fixed; bottom: 10px; text-align: center; width: 100%; color: gray;}
        </style>
        <div class="footer">Made with Streamlit | Not for medical diagnosis</div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()