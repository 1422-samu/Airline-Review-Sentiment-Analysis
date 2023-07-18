import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def airline_scrape():
    airline_names = [
        (4, "indigo-airlines", "India"),
        (3, "vistara", "India"),
        (7, "spicejet", "India"),
        (3, "airasia-india", "India"),
        (12, "air-india", "India"),
        (2, "air-india-express", "India"),
        (4, "goair", "India"),
        (24, "emirates", "UAE"),
        (8, "china-eastern-airlines", "China"),
        (9, "air-china", "China"),
        (24, "qatar-airways", "Qatar"),
        (4, "lion-air", "Indonesia"),
        (5, "japan-airlines", "Japan"),
        (7, "vietjetair", "Vietnam"),
        (7, "korean-air", "South Korea"),
        (16, "singapore-airlines", "Singapore"),
        (7, "ana-all-nippon-airways", "Japan"),
        (21, "china-southern-airlines", "China"),
        (12, "jet-airways", "India"),
    ]

    url = None
    airline = []
    country = []
    review = []
    date_published = []
    type_of_traveller = []
    seat_type = []
    route = []
    seat_comfort = []
    cabin_staff_service = []
    food_and_beverages = []
    inflight_entertainment = []
    ground_service = []
    value_for_money = []
    recommended = []

    for pages, air_name, country_name in airline_names:
        for j in range(1, pages):
            if j == 1:
                url = (
                    "https://www.airlinequality.com/airline-reviews/"
                    + f"{air_name}"
                    + "/?sortby=post_date%3ADesc&pagesize=100"
                )
            else:
                url = (
                    "https://www.airlinequality.com/airline-reviews/"
                    + f"{air_name}"
                    + "/page/"
                    + f"{j}"
                    + "/?sortby=post_date%3ADesc&pagesize=100"
                )
                pass

            # Getting the data from the website
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html5lib")

            # Get the date published of the review

            dates = soup.find_all(class_="media")
            for date in dates:
                try:
                    review_published_on = date.find("time").attrs["datetime"]
                    date_published.append(review_published_on)
                except AttributeError:
                    pass

            # Extracting the reviews and the review ratings

            articles = soup.find_all("div", class_="tc_mobile")

            for article in articles:
                review.append(
                    article.find(
                        "div", attrs={"class": "text_content", "itemprop": "reviewBody"}
                    ).text
                )

                table_rows = article.find(
                    "table", attrs={"class": "review-ratings"}
                ).find_all("tr")

                # Initialize variables to store the values
                type_of_traveller_value = np.nan
                seat_type_value = np.nan
                route_value = np.nan
                seat_comfort_value = np.nan
                cabin_staff_service_value = np.nan
                food_and_beverages_value = np.nan
                inflight_entertainment_value = np.nan
                ground_service_value = np.nan
                value_for_money_value = np.nan
                recommended_value = np.nan

                for row in table_rows:
                    try:
                        if row.find_all("td")[0].text == "Type Of Traveller":
                            type_of_traveller_value = row.find_all("td")[1].text
                        elif row.find_all("td")[0].text == "Seat Type":
                            seat_type_value = row.find_all("td")[1].text
                        elif row.find_all("td")[0].text == "Route":
                            route_value = row.find_all("td")[1].text
                        elif row.find_all("td")[0].text == "Seat Comfort":
                            seat_comfort_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Cabin Staff Service":
                            cabin_staff_service_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Food & Beverages":
                            food_and_beverages_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Inflight Entertainment":
                            inflight_entertainment_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Ground Service":
                            ground_service_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Value For Money":
                            value_for_money_value = (
                                row.find_all("td")[1]
                                .find_all("span", class_="star fill")[-1]
                                .text
                            )
                        elif row.find_all("td")[0].text == "Recommended":
                            recommended_value = row.find_all("td")[1].text
                        else:
                            pass
                    except IndexError:
                        pass

                # Append the values to the respective lists
                airline.append(air_name)
                country.append(country_name)
                type_of_traveller.append(type_of_traveller_value)
                seat_type.append(seat_type_value)
                route.append(route_value)
                seat_comfort.append(seat_comfort_value)
                cabin_staff_service.append(cabin_staff_service_value)
                food_and_beverages.append(food_and_beverages_value)
                inflight_entertainment.append(inflight_entertainment_value)
                ground_service.append(ground_service_value)
                value_for_money.append(value_for_money_value)
                recommended.append(recommended_value)
                pass
            pass

    # Create a dataframe
    df = pd.DataFrame(
        {
            "Airline": airline,
            "Country": country,
            "Review": review,
            "Date_Published": date_published,
            "Type of Traveller": type_of_traveller,
            "Seat Type": seat_type,
            "Route": route,
            "Seat Comfort": seat_comfort,
            "Cabin Staff Service": cabin_staff_service,
            "Food & Beverages": food_and_beverages,
            "Inflight Entertainment": inflight_entertainment,
            "Ground Service": ground_service,
            "Value for Money": value_for_money,
            "Recommended": recommended,
        }
    )
    return df


airline_df = airline_scrape()
airline_df.head()
airline_df.to_csv("airline_df.csv", index=False)
