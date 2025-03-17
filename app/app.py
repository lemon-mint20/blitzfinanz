import streamlit as st
import insert_data, find_data
from datetime import datetime
import yaml, pytz

def read_currencies(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['currencies']

st.title("BlitzFinance")

# Inject JavaScript to disable Enter key form submission
st.components.v1.html("""
<script>
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
});
</script>
""")

# Form for data input
with st.form(key='transaction_form'):

    dateInput = st.date_input("Date", datetime.today())
    # timeInput = st.time_input("Time", value=datetime.now().strftime('%H:%M:00'))
    timeInput = st.time_input("Time")
    dateTime = datetime.combine(dateInput, timeInput).isoformat()
    timezones = pytz.all_timezones
    timezone = st.selectbox("Timezone", timezones, index=timezones.index("Europe/Berlin")) 

    pastLocations = find_data.get_locations()
    location = st.selectbox("Location", pastLocations)

    valueAvg = find_data.get_avg_value(limit=20)
    value = st.number_input("Value", value=float(valueAvg))

    currencies = read_currencies("config.yaml")
    last_currency = find_data.get_last_currency()
    currency = st.selectbox("Currency", currencies, index=currencies.index('EUR'))

    lastDirection = find_data.get_last_direction()
    direction = st.segmented_control("Direction", ["IN", "OUT"], selection_mode="single", default=lastDirection)

    description = st.text_input("Description")
    try:
        accounts = find_data.get_accounts()
        lastAccount = find_data.get_last_account()
    except Exception as e:
        st.error(f"Error in fetching accounts: {e}")
    finally:
        accounts = ["Cash"]
        lastAccount = "Cash"
    account = st.selectbox("Account", accounts, index=accounts.index(lastAccount))

    tagsAll = find_data.get_tags()
    tags = st.multiselect("Tags", tagsAll)

    # receipt = st.file_uploader("Receipt", type=["jpg", "jpeg", "png", "pdf"])
    # receipt = st.text_input("Receipt", value=f"{dateTime.strftime('%Y%m%d_%H%M%S')}")
    # dateTime is a string, so we can't use strftime
    filename = f"{dateTime.replace(':', '').replace('-', '')}"
    receipt = st.text_input("Receipt")

    submit_button = st.form_submit_button(label='Insert Transaction')

    if submit_button:
        try:
            # Print received data for debugging
            st.write("Received Data:")
            st.write(f"dateTime: {dateTime}, location: {location}, value: {value}, currency: {currency}, "
                     f"direction: {direction}, description: {description}, account: {account}, "
                     f"tags: {tags}, receipt: {receipt}")

            insert_data.insert_transaction(
                dateTime=dateTime,
                timezone=timezone,
                location=location,
                value=value,
                currency=currency,
                direction=direction,
                description=description,
                account=account,
                tags=tags,
                receipt=receipt
            )
        except Exception as e:
            st.error(f"Error in insertion: {e}")
        else:
            st.success("Data inserted successfully")