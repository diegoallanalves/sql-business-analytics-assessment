import textwrap

import streamlit as st

st.set_page_config(
    page_title="Diego Alves | SQL Assessment",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Recruiter-facing visual design
# -----------------------------
st.markdown("""
<style>
:root {
    --ink: #102A43;
    --muted: #627D98;
    --accent: #1677FF;
    --panel: rgba(255,255,255,.78);
    --line: rgba(16,42,67,.12);
}
.block-container {
    max-width: 1280px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}
[data-testid="stSidebar"] {
    border-right: 1px solid var(--line);
}
.hero {
    padding: 2.15rem 2.35rem;
    border: 1px solid var(--line);
    border-radius: 22px;
    background:
      radial-gradient(circle at 90% 10%, rgba(22,119,255,.15), transparent 32%),
      linear-gradient(135deg, rgba(255,255,255,.96), rgba(242,247,255,.90));
    box-shadow: 0 18px 50px rgba(16,42,67,.08);
    margin-bottom: 1.4rem;
}
.eyebrow {
    font-size: .78rem;
    font-weight: 800;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #1677FF;
    margin-bottom: .55rem;
}
.hero h1 {
    color: #102A43;
    font-size: 2.55rem;
    line-height: 1.08;
    margin: 0 0 .55rem 0;
    letter-spacing: -.035em;
}
.hero .subtitle {
    color: #486581;
    font-size: 1.08rem;
    margin: 0;
}
.badges {margin-top: 1.2rem;}
.badge {
    display: inline-block;
    padding: .35rem .72rem;
    margin: .15rem .28rem .15rem 0;
    border-radius: 999px;
    border: 1px solid rgba(22,119,255,.20);
    background: rgba(22,119,255,.07);
    color: #0B5FCC;
    font-size: .82rem;
    font-weight: 700;
}
.metric-card {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    min-height: 112px;
    background: var(--panel);
}
.metric-kicker {
    color: #829AB1;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .10em;
    text-transform: uppercase;
}
.metric-main {
    color: #102A43;
    font-size: 1.05rem;
    font-weight: 750;
    margin-top: .35rem;
}
.callout {
    border-left: 4px solid #1677FF;
    border-radius: 10px;
    padding: .9rem 1rem;
    background: rgba(22,119,255,.055);
    margin: .7rem 0 1rem 0;
}
.small-note {font-size: .90rem; opacity: .82;}
h1, h2, h3 {letter-spacing: -.025em;}
h2 {color: #102A43;}
[data-testid="stCode"] {border-radius: 12px;}
hr {border-color: var(--line);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">SQL Assessment • Business Analytics</div>
  <h1>Diego Alves — SQL Test Answers</h1>
  <p class="subtitle">
    A recruiter-friendly walkthrough of my SQL solutions, assumptions and analytical reasoning
    for the Global Fidelis assessment.
  </p>
  <div class="badges">
    <span class="badge">Microsoft SQL Server</span>
    <span class="badge">T-SQL</span>
    <span class="badge">Data Analysis</span>
    <span class="badge">Attribution Logic</span>
    <span class="badge">Business Analytics</span>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-card"><div class="metric-kicker">Candidate</div><div class="metric-main">Diego Alves</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-kicker">Assessment</div><div class="metric-main">SQL / Business Analytics</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-kicker">Dialect</div><div class="metric-main">Microsoft T-SQL</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><div class="metric-kicker">Focus</div><div class="metric-main">Correctness + Reasoning</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="callout">
<strong>About this submission.</strong> The assessment did not provide a physical database.
The query pages therefore present my solution logic and SQL without claiming production results.
A separate optional synthetic dataset is included only to demonstrate and validate joins,
counting behavior, time windows and attribution logic.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Shared helper
# -----------------------------
def sql_block(code: str):
    st.code(textwrap.dedent(code).strip(), language="sql")

def section(title, question, explanation, code, notes=None):
    st.markdown(f'<div class="eyebrow">Assessment answer</div>', unsafe_allow_html=True)
    st.header(title)
    st.markdown(f"**Business question:** {question}")
    st.markdown(explanation)
    if notes:
        st.markdown(notes)
    st.subheader("SQL solution")
    sql_block(code)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### Diego Alves")
    st.caption("SQL Assessment Portfolio")
    st.divider()
    st.header("Assessment Navigation")
    page = st.radio(
        "Go to",
        [
            "Overview",
            "Data Model",
            "Question 1a",
            "Question 1b",
            "Question 2a",
            "Question 2b",
            "Question 2c",
            "Question 3a",
            "Question 3b",
            "Practice Data",
            "Key SQL Concepts",
        ],
    )
    st.divider()
    st.markdown("**Prepared by**  \nDiego Alves")
    st.markdown("**Technical focus**  \nSQL • Analytics • BI • Data")
    st.markdown(
        '<div class="small-note">The optional practice data is synthetic and is '
        'included only to demonstrate the joins and expected query behavior.</div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Pages
# -----------------------------
if page == "Overview":
    st.header("Approach")
    st.markdown("""
This assessment is solved by first understanding the **grain and relationship of each table**, then choosing joins and aggregations that preserve the business meaning.

The main principles I used were:

1. **Avoid double counting.** A user can have multiple contacts, so `COUNT(DISTINCT user_ID)` is used where the same user could appear more than once.
2. **Use the correct event timestamp.** For example, Question 2a asks for *sales in 2020*, so the filter is applied to `sale_timestamp`.
3. **Preserve zero-event groups when needed.** `LEFT JOIN` is used in Question 2c so users with no qualifying sale are still counted.
4. **Aggregate before joining daily totals.** In Question 3a, clicks and registrations are aggregated separately before being joined, preventing many-to-many row multiplication.
5. **Separate calendar-day reporting from attribution.** Question 3a measures events occurring on the same calendar day; Question 3b associates later registrations with earlier tracked click days.
""")
    st.success("The SQL below is written in Microsoft SQL Server / T-SQL.")

elif page == "Data Model":
    st.header("Data Model")
    st.markdown("""
The assignment describes six tables:

| Table | Grain / purpose |
|---|---|
| `users` | One row per registered user |
| `contacts` | User-level tracked advertising contacts/clicks |
| `channels` | Lookup from channel ID to channel name |
| `informations` | Aggregated marketing clicks and impressions; no individual user ID |
| `sales` | One row per sale |
| `payments` | Payment records linked to sales |

### Core relationships

- `contacts.contact_user_ID → users.user_ID`
- `contacts.contact_channel_ID → channels.channel_ID`
- `informations.info_channel_ID → channels.channel_ID`
- `sales.sale_user_ID → users.user_ID`
- `payments.pay_sale_ID → sales.sale_ID`

### Important distinction

`informations` contains **aggregated click totals** and cannot identify an individual customer.  
`contacts` is the **user-level bridge** that allows tracked marketing contacts to be associated with registered users.
""")
    st.markdown("""
**Channel abbreviations used in the practice data**

- `SEM` — Search Engine Marketing
- `AFF` — Affiliate Marketing
- `SOCIAL` — Social Media
- `EMAIL` — Email Marketing
""")

elif page == "Question 1a":
    section(
        "Question 1a",
        "The number of users per channel and registration date.",
        """
**Logic**

**First**, join users to their contacts.  
**Second**, join contacts to the channel lookup so the output shows readable channel names.  
**Third**, convert the registration timestamp to a date because the requested grouping is by registration date.  
**Fourth**, count distinct users.

`DISTINCT` matters because one user can have more than one contact and should not be counted twice inside the same channel/date group.
""",
        """
SELECT
    ch.channel_name,
    CAST(u.user_registration_timestamp AS DATE) AS registration_date,
    COUNT(DISTINCT u.user_ID) AS number_of_users
FROM users AS u
INNER JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
INNER JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
GROUP BY
    ch.channel_name,
    CAST(u.user_registration_timestamp AS DATE)
ORDER BY
    registration_date,
    ch.channel_name;
""",
    )

elif page == "Question 1b":
    section(
        "Question 1b",
        "What can happen if DISTINCT is omitted, why can channel totals still exceed total users, and how can the query be adjusted?",
        """
**Explanation**

**First — if `DISTINCT` is omitted:** a user with multiple contacts in the same channel can be counted multiple times.

**Second — why totals can still exceed the real user count even with `DISTINCT`:** `DISTINCT` applies inside each group. A user who interacted through both `AFF` and `SEM` can appear once in each channel. Summing the channel totals therefore counts that person twice.

**Third — one-channel attribution:** if the business requires exactly one marketing channel per user, use the contact where `contact_is_last = 1`. The assignment states that only one contact per customer is marked as last.
""",
        """
SELECT
    ch.channel_name,
    CAST(u.user_registration_timestamp AS DATE) AS registration_date,
    COUNT(*) AS number_of_users
FROM users AS u
INNER JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
   AND c.contact_is_last = 1
INNER JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
GROUP BY
    ch.channel_name,
    CAST(u.user_registration_timestamp AS DATE)
ORDER BY
    registration_date,
    ch.channel_name;
""",
        """
**Additional consideration:** users with no contacts cannot be attributed to a marketing channel. If the business wants those users shown as well, a `LEFT JOIN` can be used and the missing channel can be labelled `NO CONTACT`.
""",
    )

elif page == "Question 2a":
    section(
        "Question 2a",
        "The total pay_amount per city for sales in 2020.",
        """
**Logic**

**First**, start with `users` because the city belongs to the user.  
**Second**, join `users → sales → payments`.  
**Third**, filter by `sale_timestamp`, because the wording asks for **sales in 2020**.  
**Fourth**, sum payment amount by city.

The half-open date range (`>= 2020-01-01` and `< 2021-01-01`) safely handles timestamps containing hours, minutes, and seconds.
""",
        """
SELECT
    u.user_city,
    SUM(p.pay_amount) AS total_pay_amount
FROM users AS u
INNER JOIN sales AS s
    ON s.sale_user_ID = u.user_ID
INNER JOIN payments AS p
    ON p.pay_sale_ID = s.sale_ID
WHERE s.sale_timestamp >= '2020-01-01'
  AND s.sale_timestamp <  '2021-01-01'
GROUP BY
    u.user_city
ORDER BY
    u.user_city;
""",
    )

elif page == "Question 2b":
    section(
        "Question 2b",
        "The number of users whose last contact is SEM but who also have at least one additional contact through another channel.",
        """
**Logic**

There are two conditions:

1. The user's **last contact** must be `SEM`.
2. The same user must have **at least one other contact** where the channel is not `SEM`.

`EXISTS` is appropriate because the query only needs to know whether another qualifying contact exists; it does not need to return or aggregate all of those rows.
""",
        """
SELECT
    COUNT(DISTINCT last_c.contact_user_ID) AS number_of_users
FROM contacts AS last_c
INNER JOIN channels AS last_ch
    ON last_ch.channel_ID = last_c.contact_channel_ID
WHERE last_c.contact_is_last = 1
  AND last_ch.channel_name = 'SEM'
  AND EXISTS (
      SELECT 1
      FROM contacts AS other_c
      INNER JOIN channels AS other_ch
          ON other_ch.channel_ID = other_c.contact_channel_ID
      WHERE other_c.contact_user_ID = last_c.contact_user_ID
        AND other_ch.channel_name <> 'SEM'
  );
""",
    )

elif page == "Question 2c":
    section(
        "Question 2c",
        "Per registration date and last channel, show the number of users and the number of sales made within 3 days after registration.",
        """
**Logic**

**First**, identify each user's last channel with `contact_is_last = 1`.  
**Second**, group by registration date and that last channel.  
**Third**, `LEFT JOIN` sales so users remain in the result even if they made zero qualifying sales.  
**Fourth**, limit joined sales to the first 3 days after registration.  
**Fifth**, count users with `COUNT(DISTINCT ...)` because one user may have multiple qualifying sales.

I interpret “within 3 days” as the first **72 hours** after registration.
""",
        """
SELECT
    CAST(u.user_registration_timestamp AS DATE) AS registration_date,
    ch.channel_name AS last_channel,
    COUNT(DISTINCT u.user_ID) AS number_of_users,
    COUNT(s.sale_ID) AS number_of_sales_within_3_days
FROM users AS u
INNER JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
   AND c.contact_is_last = 1
INNER JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
LEFT JOIN sales AS s
    ON s.sale_user_ID = u.user_ID
   AND s.sale_timestamp >= u.user_registration_timestamp
   AND s.sale_timestamp < DATEADD(DAY, 3, u.user_registration_timestamp)
GROUP BY
    CAST(u.user_registration_timestamp AS DATE),
    ch.channel_name
ORDER BY
    registration_date,
    last_channel;
""",
    )

elif page == "Question 3a":
    section(
        "Question 3a",
        "The number of clicks and registrations per day in 2020.",
        """
**What this measures**

This is a **calendar-day activity view**:

- clicks that happened on each date;
- registrations that happened on each date.

A registration shown on a date is **not necessarily caused by the clicks shown on that same row**.

**Why aggregate first?** Joining raw click and registration rows could create many-to-many combinations and inflate totals. I therefore aggregate each event type by day first, then join the daily results.

A `FULL OUTER JOIN` keeps dates that have only clicks or only registrations. No calendar table is created, so days with neither event are naturally omitted.
""",
        """
WITH clicks_per_day AS (
    SELECT
        CAST(info_timestamp AS DATE) AS event_date,
        SUM(info_clicks) AS number_of_clicks
    FROM informations
    WHERE info_timestamp >= '2020-01-01'
      AND info_timestamp <  '2021-01-01'
    GROUP BY CAST(info_timestamp AS DATE)
),
registrations_per_day AS (
    SELECT
        CAST(user_registration_timestamp AS DATE) AS event_date,
        COUNT(*) AS number_of_registrations
    FROM users
    WHERE user_registration_timestamp >= '2020-01-01'
      AND user_registration_timestamp <  '2021-01-01'
    GROUP BY CAST(user_registration_timestamp AS DATE)
)
SELECT
    COALESCE(c.event_date, r.event_date) AS event_date,
    COALESCE(c.number_of_clicks, 0) AS number_of_clicks,
    COALESCE(r.number_of_registrations, 0) AS number_of_registrations
FROM clicks_per_day AS c
FULL OUTER JOIN registrations_per_day AS r
    ON r.event_date = c.event_date
ORDER BY event_date;
""",
    )

elif page == "Question 3b":
    section(
        "Question 3b",
        "The number of clicks and registrations per click day in 2020.",
        """
**What this measures**

This differs from Question 3a.

- **3a:** “What happened on each calendar day?”
- **3b:** “For each click day, how many registrations can be associated with tracked contacts from that click day?”

The `informations` table provides the **total aggregated clicks**. It has no user IDs. The `contacts` table provides the **user-level bridge** that allows a tracked contact to be associated with a registered user.

`COUNT(DISTINCT u.user_ID)` prevents one user from being counted more than once on the same click day if multiple contact rows exist.
""",
        """
WITH clicks_per_day AS (
    SELECT
        CAST(info_timestamp AS DATE) AS click_date,
        SUM(info_clicks) AS number_of_clicks
    FROM informations
    WHERE info_timestamp >= '2020-01-01'
      AND info_timestamp <  '2021-01-01'
    GROUP BY CAST(info_timestamp AS DATE)
),
registrations_by_click_day AS (
    SELECT
        CAST(c.contact_timestamp AS DATE) AS click_date,
        COUNT(DISTINCT u.user_ID) AS number_of_registrations
    FROM contacts AS c
    INNER JOIN users AS u
        ON u.user_ID = c.contact_user_ID
    WHERE c.contact_timestamp >= '2020-01-01'
      AND c.contact_timestamp <  '2021-01-01'
      AND c.contact_timestamp < u.user_registration_timestamp
    GROUP BY CAST(c.contact_timestamp AS DATE)
)
SELECT
    c.click_date,
    c.number_of_clicks,
    COALESCE(r.number_of_registrations, 0) AS number_of_registrations
FROM clicks_per_day AS c
LEFT JOIN registrations_by_click_day AS r
    ON r.click_date = c.click_date
ORDER BY c.click_date;
""",
        """
**Example**

If a tracked click occurred on **2 Jan** and the user registered on **5 Jan**:

- in **3a**, the click belongs to 2 Jan and the registration belongs to 5 Jan;
- in **3b**, that registration can be associated back to the 2 Jan click-day cohort.

**Assumption:** because `informations` is aggregated and contains no user ID, user-level attribution must use `contacts`. A user who has qualifying pre-registration contacts on different click dates can consequently be represented in more than one click-day cohort; this is click-day attribution rather than mutually exclusive user attribution.
""",
    )

elif page == "Practice Data":
    st.header("Optional Practice Data")
    st.warning(
        "This section is not presented as real Global Fidelis data. It is synthetic "
        "data created only to validate joins, counting behavior, date windows, and attribution logic."
    )
    st.markdown("""
The practice dataset deliberately includes cases such as:

- users with multiple contacts;
- users who touched multiple channels;
- one last contact per contacted user;
- a registered user with no contact;
- sales both inside and outside the 3-day registration window;
- click days with no registrations and registration days with no clicks.

This makes it possible to test why `DISTINCT`, `LEFT JOIN`, `EXISTS`, date filtering, and last-touch attribution matter.
""")
    with st.expander("Practice database and synthetic data SQL"):
        sql_block("""
IF DB_ID('GlobalFidelis_SQL_Practice') IS NULL
BEGIN
    CREATE DATABASE GlobalFidelis_SQL_Practice;
END;
GO

USE GlobalFidelis_SQL_Practice;
GO

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS informations;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS users;
GO

CREATE TABLE users (
    user_ID INT PRIMARY KEY,
    user_city VARCHAR(100) NULL,
    user_gender VARCHAR(20) NULL,
    user_registration_timestamp DATETIME2 NOT NULL
);

CREATE TABLE channels (
    channel_ID VARCHAR(20) PRIMARY KEY,
    channel_name VARCHAR(50) NOT NULL
);

CREATE TABLE contacts (
    contact_user_ID INT NOT NULL,
    contact_channel_ID VARCHAR(20) NOT NULL,
    contact_timestamp DATETIME2 NOT NULL,
    contact_is_last BIT NOT NULL,
    FOREIGN KEY (contact_user_ID) REFERENCES users(user_ID),
    FOREIGN KEY (contact_channel_ID) REFERENCES channels(channel_ID)
);

CREATE TABLE informations (
    info_channel_ID VARCHAR(20) NOT NULL,
    info_timestamp DATETIME2 NOT NULL,
    info_clicks INT NOT NULL,
    info_impressions INT NOT NULL,
    FOREIGN KEY (info_channel_ID) REFERENCES channels(channel_ID)
);

CREATE TABLE sales (
    sale_ID INT PRIMARY KEY,
    sale_user_ID INT NOT NULL,
    sale_timestamp DATETIME2 NOT NULL,
    sale_type VARCHAR(50) NULL,
    FOREIGN KEY (sale_user_ID) REFERENCES users(user_ID)
);

CREATE TABLE payments (
    pay_sale_ID INT NOT NULL,
    pay_timestamp DATETIME2 NOT NULL,
    pay_amount DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (pay_sale_ID) REFERENCES sales(sale_ID)
);
GO

INSERT INTO channels (channel_ID, channel_name) VALUES
('CH01', 'SEM'),
('CH02', 'AFF'),
('CH03', 'SOCIAL'),
('CH04', 'EMAIL');

INSERT INTO users VALUES
(1, 'London', 'M', '2020-01-05T10:00:00'),
(2, 'Manchester', 'F', '2020-01-05T11:30:00'),
(3, 'London', 'F', '2020-01-06T09:00:00'),
(4, 'Bristol', NULL, '2020-02-10T15:00:00'),
(5, 'London', 'M', '2021-01-03T12:00:00'),
(6, 'Leeds', 'F', '2020-02-10T18:00:00');

INSERT INTO contacts VALUES
(1, 'CH02', '2020-01-02T08:00:00', 0),
(1, 'CH01', '2020-01-04T14:00:00', 1),
(2, 'CH01', '2020-01-03T09:00:00', 1),
(3, 'CH03', '2020-01-03T10:00:00', 0),
(3, 'CH01', '2020-01-05T12:00:00', 1),
(5, 'CH03', '2021-01-02T11:00:00', 1),
(6, 'CH01', '2020-02-07T13:00:00', 0),
(6, 'CH02', '2020-02-09T16:00:00', 1);

INSERT INTO informations VALUES
('CH02', '2020-01-02T08:00:00', 10, 200),
('CH01', '2020-01-03T09:00:00', 15, 300),
('CH03', '2020-01-03T10:00:00', 7, 150),
('CH01', '2020-01-04T14:00:00', 20, 400),
('CH01', '2020-01-05T12:00:00', 12, 250),
('CH01', '2020-02-07T13:00:00', 9, 180),
('CH02', '2020-02-09T16:00:00', 6, 120),
('CH03', '2021-01-02T11:00:00', 5, 100);

INSERT INTO sales VALUES
(101, 1, '2020-01-06T12:00:00', 'standard'),
(102, 1, '2020-01-20T12:00:00', 'standard'),
(103, 2, '2020-01-07T09:00:00', 'standard'),
(104, 3, '2020-01-09T13:00:00', 'standard'),
(105, 4, '2020-02-12T10:00:00', 'standard'),
(106, 5, '2021-01-05T10:00:00', 'standard'),
(107, 6, '2020-02-20T10:00:00', 'standard');

INSERT INTO payments VALUES
(101, '2020-01-06T12:05:00', 120.00),
(102, '2020-01-20T12:05:00', 80.00),
(103, '2020-01-07T09:05:00', 200.00),
(104, '2020-01-09T13:05:00', 75.00),
(105, '2020-02-12T10:05:00', 300.00),
(106, '2021-01-05T10:05:00', 500.00),
(107, '2020-02-20T10:05:00', 150.00);
GO
""")

elif page == "Key SQL Concepts":
    st.header("Key SQL Concepts Demonstrated")
    st.markdown("""
### `CAST(... AS DATE)`
Removes the time portion of a timestamp for date-level grouping. It does **not** change the stored source value; it changes how the expression is treated in the query.

### `COUNT(DISTINCT ...)`
Counts each user only once inside a group, which is important when joins can produce several rows for one user.

### `INNER JOIN`
Keeps rows that have matching records on both sides.

### `LEFT JOIN`
Keeps all rows from the left side even if there is no matching row on the right. This is why it is useful when users with zero qualifying sales must remain visible.

### `EXISTS`
Tests whether at least one matching row exists. It is efficient and clear when the business question is “does this user have another qualifying contact?”

### `COALESCE`
Returns the first non-null value. Here it is used to turn missing daily counts into `0` and to combine dates from a `FULL OUTER JOIN`.

### CTE (`WITH ... AS`)
Creates a named intermediate query. In Question 3a and 3b it makes the logic easier to read and, importantly, lets each metric be aggregated before the final join.

### `DATEADD`
Adds a time interval to a timestamp. In Question 2c:
`DATEADD(DAY, 3, user_registration_timestamp)` defines the end of the 72-hour window.

### Why use `< '2021-01-01'` instead of `<= '2020-12-31'`?
Timestamp columns can contain times such as `2020-12-31 18:30:00`. The half-open interval includes all of 2020 without having to guess the final possible time of 31 December.
""")

st.divider()
st.markdown("""
<div style="text-align:center; padding:1.1rem 0 .4rem 0; color:#829AB1; font-size:.88rem;">
<strong>Diego Alves</strong> · SQL Assessment Answers · Business Analytics<br>
Solutions, assumptions and reasoning presented transparently for review.
</div>
""", unsafe_allow_html=True)
