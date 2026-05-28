def run_chatbot():
    import streamlit as st
    import time
    import random
    from components.api_client import get_dashboard

    st.header("🤖 AI Health Assistant")

    # =========================
    # SESSION INIT
    # =========================
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "context" not in st.session_state:
        st.session_state.context = {}

    # =========================
    # GET USER DATA
    # =========================
    token = st.session_state.get("token")
    user_data = None

    if token:
        user_data = get_dashboard(token)

    heart = user_data.get("heart") if user_data else None
    fitness = user_data.get("fitness") if user_data else None

    # =========================
    # SHOW HISTORY
    # =========================
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # =========================
    # BOT LOGIC
    # =========================
    def get_response(user_input):
        text = user_input.lower()

        # CONTEXT DETECTION
        if "heart" in text:
            st.session_state.context["topic"] = "heart"
        elif "fitness" in text or "fit" in text:
            st.session_state.context["topic"] = "fitness"
        elif "improve" in text:
            st.session_state.context["topic"] = "improve"

        topic = st.session_state.context.get("topic")

        # =========================
        # RESPONSES
        # =========================

        # GREETING
        if any(x in text for x in ["hi", "hello", "hey"]):
            return random.choice([
                "Hey! I'm here to help you understand your health 😊",
                "Hello! Ask me anything about your fitness or heart 💪",
                "Hi! Let's improve your health step by step 🚀"
            ])

        # PERSONAL HEALTH
        if "my health" in text or "my result" in text:
            return f"""
Here’s your current health summary:

❤️ Heart: **{heart if heart else 'Unknown'}**  
🏋️ Fitness: **{fitness if fitness else 'Unknown'}**

Would you like suggestions to improve it?
"""

        # HEART
        if topic == "heart":
            if heart == "High Risk":
                return """
Your heart risk is currently **high**, but don’t worry—this is manageable.

Start with:
• 30 min walking daily  
• reduce oily & junk food  
• monitor BP regularly  

Would you like a daily routine plan?
"""
            elif heart == "Moderate Risk":
                return """
Your heart condition is **moderate**.

With consistent exercise and better diet, you can easily improve it.

Want a step-by-step improvement plan?
"""
            elif heart == "Low Risk":
                return """
Good news! Your heart health looks **stable**.

Just maintain:
• active lifestyle  
• balanced diet  
• proper sleep  

Consistency is key 👍
"""
            else:
                return "Heart health depends on BP, cholesterol, and lifestyle."

        # FITNESS
        if topic == "fitness":
            if fitness == "Unfit":
                return """
Your fitness level is currently low—but it's completely fixable 💪

Start with:
• daily walking  
• light workouts  
• better diet  

Small steps → big results.
"""
            elif fitness == "Moderate":
                return """
You are at a **moderate fitness level**.

Just increase consistency and strength training—you’ll reach fit soon.
"""
            elif fitness == "Fit":
                return """
Great job! You are **fit** 🎉

To improve further:
• focus on strength  
• improve endurance  
• maintain routine
"""
            else:
                return "Fitness depends on strength, flexibility, and endurance."

        # IMPROVE
        if topic == "improve":
            return """
To improve your health:

1. Exercise daily (30 min)  
2. Eat clean (less sugar/oil)  
3. Sleep 7–8 hours  
4. Stay hydrated  

Consistency matters more than intensity.
"""

        # BMI
        if "bmi" in text:
            return "BMI tells your body fat level. Ideal range is 18.5 – 24.9."

        # YES FOLLOW-UP
        if "yes" in text:
            return """
Great 👍 Here's a simple daily plan:

Morning → walk or stretch  
Afternoon → balanced meal  
Evening → light workout  

Stay consistent—you’ll see results.
"""

        # FALLBACK
        return random.choice([
            "I can guide you on heart health, fitness, or improvement plans.",
            "Try asking about your health, BMI, or how to improve.",
            "I'm here to help—ask me anything about your health."
        ])

    # =========================
    # STREAM EFFECT
    # =========================
    def stream(text):
        placeholder = st.empty()
        full = ""

        for word in text.split():
            full += word + " "
            placeholder.markdown(full)
            time.sleep(0.01)

        return full

    # =========================
    # QUICK BUTTONS
    # =========================
    st.markdown("### 💡 Quick Actions")

    c1, c2, c3 = st.columns(3)

    if c1.button("📊 My Health"):
        st.session_state.quick = "my health"

    if c2.button("💪 Improve"):
        st.session_state.quick = "improve"

    if c3.button("❤️ Heart"):
        st.session_state.quick = "heart"

    # =========================
    # INPUT
    # =========================
    user_input = None

    chat_input = st.chat_input("Ask something...")

    if "quick" in st.session_state:
        user_input = st.session_state.quick
        del st.session_state.quick
    elif chat_input:
        user_input = chat_input

    # =========================
    # CHAT FLOW
    # =========================
    if user_input:

        # USER
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        # BOT
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(0.3)

            response = get_response(user_input)
            final = stream(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": final
        })

    # =========================
    # CLEAR BUTTON
    # =========================
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()