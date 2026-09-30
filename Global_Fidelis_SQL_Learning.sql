/* Diego Alves - Contact: diegoarpalves@gmail.com

-- Click ctrl + F and search for this: "STEP" .THEN YOU WILL THE STEPS. 
===============================================================================
GLOBAL FIDELIS - SQL ASSIGNMENT - LEARNING VERSION FOR SQL SERVER / SSMS
Prepared for: Diego Alves
Dialect: Microsoft SQL Server (T-SQL)

PURPOSE
-------
This script is for LEARNING and local testing in SQL Server Management Studio.
The assignment itself states that no physical database is provided and recommends
not relying on sample data. Therefore:

  1) SECTION A creates OPTIONAL FAKE DATA only so you can see how the joins work.
  2) SECTION B contains the actual assignment-style queries.
  3) The comments explain WHY each part exists.

Do NOT submit the fake-data section as part of the assignment unless requested.
===============================================================================
*/

/* ============================================================================
   SECTION A - OPTIONAL PRACTICE DATABASE + FAKE DATA
   ============================================================================ */

--  STEP 1:
-- Create a separate learning database. Run this only on your own SQL Server.
IF DB_ID('GlobalFidelis_SQL_Practice') IS NULL
BEGIN
    CREATE DATABASE GlobalFidelis_SQL_Practice;
END;
GO

USE GlobalFidelis_SQL_Practice;
GO

-- Clean up old practice tables so this script can be rerun.
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS informations;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS users;
GO
-- >>> Run the query above up to this point <<<

-- STEP 2: 
-- Create the nescessary tables for the task:

/* ---------------------------------------------------------------------------
   TABLE: users
   One row is created when a customer registers.
--------------------------------------------------------------------------- */
CREATE TABLE users (
    user_ID INT PRIMARY KEY,
    user_city VARCHAR(100) NULL,
    user_gender VARCHAR(20) NULL,
    user_registration_timestamp DATETIME2 NOT NULL
);

/* ---------------------------------------------------------------------------
   TABLE: channels
   Lookup table translating channel IDs into names such as SEM or AFF.
--------------------------------------------------------------------------- */
CREATE TABLE channels (
    channel_ID VARCHAR(20) PRIMARY KEY,
    channel_name VARCHAR(50) NOT NULL
);

/* ---------------------------------------------------------------------------
   TABLE: contacts
   Individual tracked advertisement clicks that can be linked to registered users.
   A user can have MANY contacts.
   Exactly one contact per user is marked contact_is_last = 1 at a point in time.
--------------------------------------------------------------------------- */
CREATE TABLE contacts (
    contact_user_ID INT NOT NULL,
    contact_channel_ID VARCHAR(20) NOT NULL,
    contact_timestamp DATETIME2 NOT NULL,
    contact_is_last BIT NOT NULL,
    CONSTRAINT FK_contacts_users
        FOREIGN KEY (contact_user_ID) REFERENCES users(user_ID),
    CONSTRAINT FK_contacts_channels
        FOREIGN KEY (contact_channel_ID) REFERENCES channels(channel_ID)
);

/* ---------------------------------------------------------------------------
   TABLE: informations
   Aggregated advertisement activity by timestamp + channel.
   IMPORTANT: this table does NOT contain individual user IDs.
--------------------------------------------------------------------------- */
CREATE TABLE informations (
    info_channel_ID VARCHAR(20) NOT NULL,
    info_timestamp DATETIME2 NOT NULL,
    info_clicks INT NOT NULL,
    info_impressions INT NOT NULL,
    CONSTRAINT FK_information_channels
        FOREIGN KEY (info_channel_ID) REFERENCES channels(channel_ID)
);

/* ---------------------------------------------------------------------------
   TABLE: sales
   One row for each purchase made by a registered user.
--------------------------------------------------------------------------- */
CREATE TABLE sales (
    sale_ID INT PRIMARY KEY,
    sale_user_ID INT NOT NULL,
    sale_timestamp DATETIME2 NOT NULL,
    sale_type VARCHAR(50) NULL,
    CONSTRAINT FK_sales_users
        FOREIGN KEY (sale_user_ID) REFERENCES users(user_ID)
);

/* ---------------------------------------------------------------------------
   TABLE: payments
   A row exists when a sale/item is paid.
--------------------------------------------------------------------------- */
CREATE TABLE payments (
    pay_sale_ID INT NOT NULL,
    pay_timestamp DATETIME2 NOT NULL,
    pay_amount DECIMAL(12,2) NOT NULL,
    CONSTRAINT FK_payments_sales
        FOREIGN KEY (pay_sale_ID) REFERENCES sales(sale_ID)
);
GO
-- >>> Run the query above up to this point <<<

-- STEP 3:
-- Create the fake data:
-- ---------------------------------------------------------------------------
-- FAKE CHANNELS
-- ---------------------------------------------------------------------------
INSERT INTO channels (channel_ID, channel_name) VALUES
('CH01', 'SEM'),
('CH02', 'AFF'),
('CH03', 'SOCIAL'),
('CH04', 'EMAIL');

-- ---------------------------------------------------------------------------
-- FAKE USERS
-- ---------------------------------------------------------------------------
INSERT INTO users (user_ID, user_city, user_gender, user_registration_timestamp) VALUES
(1, 'London', 'M', '2020-01-05T10:00:00'),
(2, 'Manchester', 'F', '2020-01-05T11:30:00'),
(3, 'London', 'F', '2020-01-06T09:00:00'),
(4, 'Bristol', NULL, '2020-02-10T15:00:00'),
(5, 'London', 'M', '2021-01-03T12:00:00'),
(6, 'Leeds', 'F', '2020-02-10T18:00:00');

-- ---------------------------------------------------------------------------
-- FAKE CONTACTS
-- Notice:
--   * User 1 has AFF then SEM. SEM is the last contact.
--   * User 2 has only SEM.
--   * User 3 has SOCIAL then SEM. SEM is the last contact.
--   * User 4 has no contact (allowed by the assignment).
--   * User 6 has SEM then AFF. AFF is the last contact.
-- This deliberately creates multiple contacts so DISTINCT/attribution matter.
-- ---------------------------------------------------------------------------
INSERT INTO contacts
(contact_user_ID, contact_channel_ID, contact_timestamp, contact_is_last) VALUES
(1, 'CH02', '2020-01-02T08:00:00', 0),
(1, 'CH01', '2020-01-04T14:00:00', 1),
(2, 'CH01', '2020-01-03T09:00:00', 1),
(3, 'CH03', '2020-01-03T10:00:00', 0),
(3, 'CH01', '2020-01-05T12:00:00', 1),
(5, 'CH03', '2021-01-02T11:00:00', 1),
(6, 'CH01', '2020-02-07T13:00:00', 0),
(6, 'CH02', '2020-02-09T16:00:00', 1);

-- ---------------------------------------------------------------------------
-- FAKE AGGREGATED MARKETING INFORMATION
-- ---------------------------------------------------------------------------
INSERT INTO informations
(info_channel_ID, info_timestamp, info_clicks, info_impressions) VALUES
('CH02', '2020-01-02T08:00:00', 10, 200),
('CH01', '2020-01-03T09:00:00', 15, 300),
('CH03', '2020-01-03T10:00:00', 7, 150),
('CH01', '2020-01-04T14:00:00', 20, 400),
('CH01', '2020-01-05T12:00:00', 12, 250),
('CH01', '2020-02-07T13:00:00', 9, 180),
('CH02', '2020-02-09T16:00:00', 6, 120),
('CH03', '2021-01-02T11:00:00', 5, 100);

-- ---------------------------------------------------------------------------
-- FAKE SALES + PAYMENTS
-- Some sales are within 3 days of registration; some are later.
-- ---------------------------------------------------------------------------
INSERT INTO sales (sale_ID, sale_user_ID, sale_timestamp, sale_type) VALUES
(101, 1, '2020-01-06T12:00:00', 'standard'), -- within 3 days
(102, 1, '2020-01-20T12:00:00', 'standard'), -- later
(103, 2, '2020-01-07T09:00:00', 'standard'), -- within 3 days
(104, 3, '2020-01-09T13:00:00', 'standard'), -- within 3 days
(105, 4, '2020-02-12T10:00:00', 'standard'), -- within 3 days, no contact
(106, 5, '2021-01-05T10:00:00', 'standard'), -- 2021
(107, 6, '2020-02-20T10:00:00', 'standard'); -- later

INSERT INTO payments (pay_sale_ID, pay_timestamp, pay_amount) VALUES
(101, '2020-01-06T12:05:00', 120.00),
(102, '2020-01-20T12:05:00', 80.00),
(103, '2020-01-07T09:05:00', 200.00),
(104, '2020-01-09T13:05:00', 75.00),
(105, '2020-02-12T10:05:00', 300.00),
(106, '2021-01-05T10:05:00', 500.00),
(107, '2020-02-20T10:05:00', 150.00);
GO

-- >>> Run the query above up to this point <<<

-- STEP 4:
/* ============================================================================
   SECTION B - ASSIGNMENT QUERIES
   ============================================================================ */

/* ============================================================================
QUESTION 1a
"The number of users per channel and registration date"

WHAT IT MEANS
-------------
We need:
  * channel
  * registration date
  * number of users

A user can have several contacts, so COUNT(DISTINCT user_ID) prevents the same
user being counted twice inside the same channel/date group.
============================================================================ */
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
GO

-- >>> Run the query above up to this point <<<

-- STEP 5:
/* ============================================================================
QUESTION 1b
"What could happen if DISTINCT is omitted? Why does the correct number of users
not match the sum of users in this result, even if every user had a contact, and
how would you adjust the query to fix it?"

SHORT EXPLANATION
-----------------
1) If DISTINCT is omitted:
   A user with multiple contacts in the SAME channel can be counted multiple times.

2) Why can the sum across channels still exceed the real number of users even
   WITH DISTINCT?
   DISTINCT works inside each GROUP. A user who touched AFF and SEM appears once
   in AFF and once in SEM. Adding channel totals therefore counts that user twice.

3) How to fix attribution:
   If the business wants exactly ONE channel per user, use the last contact.
   The assignment says contact_is_last is true for only one row per customer.

NOTE
----
Users with no contacts still cannot be assigned to a marketing channel. If the
business wants them visible too, use LEFT JOIN and label them 'NO CONTACT'.
============================================================================ */

-- 1b FIX: ONE CHANNEL PER USER = LAST-CONTACT ATTRIBUTION
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
GO

-- OPTIONAL VERSION: INCLUDE USERS WHO HAVE NO CONTACT
SELECT
    COALESCE(ch.channel_name, 'NO CONTACT') AS channel_name,
    CAST(u.user_registration_timestamp AS DATE) AS registration_date,
    COUNT(*) AS number_of_users
FROM users AS u
LEFT JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
   AND c.contact_is_last = 1
LEFT JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
GROUP BY
    COALESCE(ch.channel_name, 'NO CONTACT'),
    CAST(u.user_registration_timestamp AS DATE)
ORDER BY
    registration_date,
    channel_name;
GO
-- >>> Run the query above up to this point <<<

-- STEP 6:
/* ============================================================================
QUESTION 2a
"The total pay_amount per city for sales in 2020"

LOGIC
-----
users -> sales -> payments

We filter by SALE date because the question says "sales in 2020".
Using >= 2020-01-01 AND < 2021-01-01 is robust and avoids problems caused by
hours/minutes/seconds in timestamps.
============================================================================ */
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
GO

-- >>> Run the query above up to this point <<<

-- STEP 7:
/* ============================================================================
QUESTION 2b
"The number of users, for whom the last contact has channel_name 'SEM', but who
have also at least one additional contact with another channel"

LOGIC
-----
Condition 1: user's LAST contact is SEM.
Condition 2: same user has AT LEAST ONE other contact whose channel is not SEM.

EXISTS is useful because we only care whether another qualifying row exists.
============================================================================ */
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
GO
-- >>> Run the query above up to this point <<<

-- STEP 8:
/* ============================================================================
QUESTION 2c
"Per registration date and last channel, the number of users and the number of
sales done by users within 3 days after the registration"

INTERPRETATION USED
-------------------
Output dimensions:
  * registration_date
  * last_channel

Aggregations:
  * number_of_users
  * number_of_sales_within_3_days

IMPORTANT
---------
Joining users directly to sales creates multiple rows per user when they have
multiple sales. Therefore users must be counted DISTINCT.

The time window below means:
  sale_timestamp >= registration timestamp
  sale_timestamp < registration timestamp + 3 days

This treats "within 3 days" as the first 72 hours after registration.
============================================================================ */
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
GO
-- >>> Run the query above up to this point <<<

-- STEP 9:
/* ============================================================================
QUESTION 3a
"The number of clicks and registrations per day in 2020"

WHAT THIS MEASURES
------------------
Calendar-day activity:
  * clicks that HAPPENED on each day
  * registrations that HAPPENED on each day

These two measures are independent daily totals. A click on Jan 2 and a later
registration on Jan 5 remain on their respective event dates.

WHY WE AGGREGATE FIRST
----------------------
If we joined raw rows first, many-to-many combinations could multiply counts.
So we aggregate clicks by day and registrations by day BEFORE joining.

The assignment says not to create a calendar and to skip days without results.
FULL OUTER JOIN preserves days that have only clicks or only registrations.
============================================================================ */
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
GO

-- >>> Run the query above up to this point <<<

-- STEP 10:
/* ============================================================================
QUESTION 3b
"The number of clicks and registrations per click day in 2020"

WHAT THIS MEASURES
------------------
This is different from 3a.

3a asks:
  "What happened on each calendar day?"

3b asks, conceptually:
  "For the clicks from each click day, how many registrations can be associated
   with those click-day contacts?"

The informations table provides ALL aggregated clicks, while contacts provides
individual tracked clicks that can be associated with users after registration.
Therefore:
  * total clicks come from informations
  * registrations attributable to a click day come from contacts + users

A user may have more than one contact on the same day. COUNT(DISTINCT user_ID)
prevents counting the same registration multiple times for that click day.
============================================================================ */
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
      -- A contact created before registration can be interpreted as a click
      -- contributing to that later registration.
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
GO
-- >>> Run the query above up to this point <<<

-- STEP 11:
/* ============================================================================
WRITTEN EXPLANATION FOR QUESTION 3b
-------------------------------------------------------------------------------
3a measures DAILY PLATFORM ACTIVITY:
    clicks occurring on a date versus registrations occurring on that same date.
    The registrations do not have to come from those clicks.

3b measures CLICK-DAY / COHORT ATTRIBUTION:
    clicks are grouped by the day the click happened, and registrations are
    associated back to the earlier tracked click day through contacts.

Example:
    Click:        02 Jan
    Registration: 05 Jan

    In 3a:
      02 Jan gets the click.
      05 Jan gets the registration.

    In 3b:
      The registration can be associated with the 02 Jan click day.
============================================================================ */
-- >>> Run the query above up to this point <<<

-- STEP 12:
/* ============================================================================
BONUS LEARNING QUERIES
These are NOT requested by the assignment. Use them to understand the data.
============================================================================ */

-- See every user and their contacts.
SELECT
    u.user_ID,
    u.user_registration_timestamp,
    ch.channel_name,
    c.contact_timestamp,
    c.contact_is_last
FROM users AS u
LEFT JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
LEFT JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
ORDER BY u.user_ID, c.contact_timestamp;
GO

-- Compare raw contact count with distinct users by channel.
SELECT
    ch.channel_name,
    COUNT(*) AS contact_rows,
    COUNT(DISTINCT c.contact_user_ID) AS distinct_users
FROM contacts AS c
INNER JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
GROUP BY ch.channel_name;
GO

-- Show each user's last attributed channel.
SELECT
    u.user_ID,
    COALESCE(ch.channel_name, 'NO CONTACT') AS last_channel
FROM users AS u
LEFT JOIN contacts AS c
    ON c.contact_user_ID = u.user_ID
   AND c.contact_is_last = 1
LEFT JOIN channels AS ch
    ON ch.channel_ID = c.contact_channel_ID
ORDER BY u.user_ID;
GO

-- Show sales and whether they occurred within 3 days after registration.
SELECT
    u.user_ID,
    u.user_registration_timestamp,
    s.sale_ID,
    s.sale_timestamp,
    CASE
        WHEN s.sale_timestamp >= u.user_registration_timestamp
         AND s.sale_timestamp < DATEADD(DAY, 3, u.user_registration_timestamp)
        THEN 'WITHIN 3 DAYS'
        ELSE 'OUTSIDE 3 DAYS'
    END AS sale_window
FROM users AS u
INNER JOIN sales AS s
    ON s.sale_user_ID = u.user_ID
ORDER BY u.user_ID, s.sale_timestamp;
GO

/* ============================================================================
END OF LEARNING SCRIPT
============================================================================ */
