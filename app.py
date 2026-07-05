import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", app_title="DH Food Wastage Report")


@app.cell
def _():
    import marimo as mo 
    import pandas as pd 
    import altair as alt

    return alt, mo, pd


@app.cell
def _(pd):
    data = pd.read_csv('food wastage dataset.csv')
    #fix date
    data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')
    #melting dow the data for easy plotting
    data_melted = data.melt(id_vars=['date'], value_vars=['lunch', 'supper'], 
                            var_name='Meal', value_name='Wastage')

    return data, data_melted


@app.cell(hide_code=True)
def _(mo):
    def introduction():
        return mo.md(
            """
            # DH Food Wastage Report Project
            **Presented by:** The Science, Technology, and Innovation Club
        
        
            ---
        
            ###  How This Project Started
            This project began as a small initiative within our club. We noticed the amount of food left on plates and wanted to understand exactly how much was being wasted. 
        
            Instead of just guessing, we decided to use the coding and data analysis skills we have been learning. Over the course of two weeks, we actively tracked the dining hall numbers, wrote the Python code to process the data, and built this interactive dashboard to share our findings with you.
        
            **Our goal was simple:** Use technology to help Kiira College Butiki become more efficient and sustainable. Every kilogram of wasted food represents a lost budget that could be reinvested into better student resources.


            ##  Explore the Data
        
            We remaind everyone that **this entire report is a live, interactive tool**. 
        
            It is not just a slideshow. We built this for *you* to use:
            * **Hover** over any bar or line to see the exact number of units wasted.
            * **Click and drag** on the timeline (Question 8) to zoom in on specific weeks.
            * **Ask questions!** If you want to know what happened on a specific Tuesday, we can pull up the exact data right now.
        
            We invite you to play with the graphs and help us find more insights we forgot to get.
            """
        )
    introduction()
    return


@app.cell
def _(alt, data, mo):
    def section_1_overall_waste(df):
        # 1. The Question
        question = mo.md(
            """
            ## Question 1: How much food are we actually wasting overall?
            Before we look at specific days, we need to understand the total scale of our food wastage across lunch and supper.
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('value:Q', title='Total Units Wasted'),
            color=alt.Color('Meal:N', scale=alt.Scale(domain=['lunch', 'supper'], range=['#ff7f0e', '#1f77b4'])),
            tooltip=['date:T', 'Meal:N', 'value:Q']
        ).transform_fold(
            ['lunch', 'supper'],
            as_=['Meal', 'value']
        ).properties(
           width='container',
            height=350,
            title="Total Daily Food Waste Volume"
        ).interactive()
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ### What this graph tells us:
            Over the 16 days tracked, we wasted a total of **3,462.77 kg** of food. 
            * **Lunch** accounts for the majority of this waste (1,885.29 kg).
            * **Supper** accounts for slightly less (1,577.48 kg). 
            * Looking at the stacked bars, you can easily see our overall footprint. While most days hover around the same total volume, there is a massive drop on June 18th and June 25th. We need to investigate what caused those successful, low-waste days!
            """
        )
    
        return mo.vstack([question, graph, explanation])

    section_1_overall_waste(data)
    return


@app.cell
def _(alt, data, data_melted, mo):
    def section_2_trends(df):

        # 1. The Question
        question = mo.md(
            """
            ---
            ## Question 2: Is our food wastage getting better or worse?
            Are there specific spikes during the month that we should be worried about? If we look at the day-to-day trend.
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(data_melted).mark_line(point=True).encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Wastage:Q', title='Units Wasted (kg)'),
            color=alt.Color('Meal:N', scale=alt.Scale(domain=['lunch', 'supper'], range=['#ff7f0e', '#1f77b4'])),
            tooltip=['date:T', 'Meal:N', 'Wastage:Q']
        ).properties(
            width='container',
            height=350,
            title="Daily Wastage Trend (Lunch vs. Supper)"
        ).interactive()
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ###  What this graph tells us:
            Our waste is not steadily increasing or decreasing; rather, it is highly erratic—especially for lunch.
            * The **orange line (lunch)** shows drastic peaks and valleys. This suggests that students either love or hate the lunch menu depending on the day.
            * The **blue line (supper)** is much more stable, generally hovering around 120 kg, except for exactly two days where it plummeted to zero. 
            * **Action point:** There is need to cross-reference the peaks on this line chart with the mess menu to identify why sometimes the meals are unpopular.
            """
        )
    
        return mo.vstack([question, graph, explanation])

    section_2_trends(data)
    return


@app.cell
def _():
    return


@app.cell
def _(alt, data, mo):
    def section_3_day_of_week(df):
        # Add day of week and calculate averages
        df['Day'] = df['date'].dt.day_name()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_avg = df.groupby('Day')[['lunch', 'supper']].mean().reset_index()
        dow_melted = dow_avg.melt(id_vars='Day', var_name='Meal', value_name='Average Waste')

        # 1. The Question
        question = mo.md(
            """
            ---
            ## Question 3: Are certain days of the week worse than others?
            Since our menus operate on a weekly rotation, let's see which days of the week produce the most waste on average.
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(dow_melted).mark_bar().encode(
            x=alt.X('Day:N', sort=days, title='Day of the Week'),
            y=alt.Y('Average Waste:Q', title='Average Units Wasted'),
            color=alt.Color('Meal:N', scale=alt.Scale(domain=['lunch', 'supper'], range=['#ff7f0e', '#1f77b4'])),
            xOffset='Meal:N',
            tooltip=['Day:N', 'Meal:N', 'Average Waste:Q']
        ).properties(
            width='container',
            height=350,
            title="Average Waste by Day of the Week"
        )
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ### What this graph tells us:
            This is perhaps the most actionable insight for the kitchen staff, as it clearly reveals weekly habits.
            * **Thursdays are fantastic:** We have incredibly low waste on Thursdays.  We were suprised it wasn't Wednesday. Whatever is being done on Thursday needs to continuew.
            * **Sundays are mixed:** Lunch waste drops significantly on Sundays, but supper waste goes up.
            * **Tuesdays and Fridays are our trouble spots:** These days generate the highest combined waste.
            """
        )
    
        return mo.vstack([question, graph, explanation])

    section_3_day_of_week(data)
    return


@app.cell
def _(alt, data, mo, pd):
    def section_4_proportions(df):
        # Prepare data for pie/donut chart
        total_lunch = df['lunch'].sum()
        total_supper = df['supper'].sum()
    
        source = pd.DataFrame({
            "Meal": ["Lunch", "Supper"],
            "Total Waste": [total_lunch, total_supper]
        })

        # 1. The Question
        question = mo.md(
            """
            ---
            ##  Question 4: Which meal is our biggest problem area?
            If we have limited time to redesign our menus, should we focus our efforts on lunch or supper?
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Total Waste", type="quantitative"),
            color=alt.Color(field="Meal", type="nominal", scale=alt.Scale(domain=['Lunch', 'Supper'], range=['#ff7f0e', '#1f77b4'])),
            tooltip=['Meal', 'Total Waste']
        ).properties(
            width='container',
            height=350,
            title="Proportion of Total Waste (Lunch vs. Supper)"
        )
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ### What this graph tells us:
            Over the tracked period, **Lunch** is the bigger culprit, making up **54.4%** of our total waste, while **Supper** makes up **45.6%**.
            * While both meals contribute significantly, lunch is clearly the heavier burden on our food waste management. 
       
            """
        )
    
        return mo.vstack([question, graph, explanation])
    section_4_proportions(data)
    return


@app.cell
def _(alt, data, mo):
    def section_5_consistency(df):
        # Melt data for the box plot
        df_melted = df.melt(id_vars=['date'], value_vars=['lunch', 'supper'], 
                            var_name='Meal', value_name='Wastage')

        # 1. The Question
        question = mo.md(
            """
            ---
            ##  Question 5: How predictable is our food waste?
            Does the amount of waste stay the same every day, or does it fluctuate wildly? Understanding this helps our kitchen prepare the right amount of food.
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(df_melted).mark_boxplot(extent='min-max').encode(
            x=alt.X('Meal:N', title='Meal Time'),
            y=alt.Y('Wastage:Q', title='Units Wasted'),
            color=alt.Color('Meal:N', legend=None, scale=alt.Scale(domain=['lunch', 'supper'], range=['#ff7f0e', '#1f77b4'])),
            tooltip=['Meal', 'min(Wastage)', 'max(Wastage)', 'median(Wastage)']
        ).properties(
            width='container',
            height=400,
            title="Volatility of Waste (Lunch vs Supper)"
        ).interactive()
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ###  What this graph tells us:
            This box plot shows the spread and consistency of our waste.
            * **Supper (Blue):** The box is relatively compact, meaning supper waste is fairly consistent from day to day (usually hovering around 120 kg). The long line stretching down shows the rare outlier days where waste dropped to zero.
            * **Lunch (Orange):** The box and the lines stretch out much further. This means lunch waste is highly volatile and unpredictable. Some days it is very low, and some days it is extremely high.
            """
        )
    
        return mo.vstack([question, graph, explanation])

    section_5_consistency(data)
    return


@app.cell
def _(alt, data, mo):
    def section_6_correlation(df):
        # 1. The Question
        question = mo.md(
            """
            ---
            ##  Question 6: Do high-waste lunches lead to high-waste suppers?
            We want to know if waste is isolated to specific meals, or if there are overall "bad days" where students just aren't eating what we serve all day long.
            """
        )
    
        # 2. The Graph (ULTRA-SAFE FIX)
        # Step A: Define the base coordinates first
        base = alt.Chart(df).encode(
            x=alt.X('lunch:Q', title='Lunch Waste (kg)', scale=alt.Scale(zero=False)),
            y=alt.Y('supper:Q', title='Supper Waste (kg)', scale=alt.Scale(zero=False))
        )
    
        # Step B: Draw the circles and add tooltips ONLY to the circles
        scatter = base.mark_circle(size=100, color='#9467bd', opacity=0.8).encode(
            tooltip=['date:T', 'lunch:Q', 'supper:Q']
        )
    
        # Step C: Draw the trendline purely from the base data
        trend = base.transform_regression('lunch', 'supper').mark_line(color='red')
    
        # Step D: Layer them together and set properties (NO .interactive() call here)
        chart = (scatter + trend).properties(
            width='container',
            height=400,
            title="Lunch vs. Supper Waste Correlation"
        )
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ###  What this graph tells us:
            This scatter plot shows the relationship between lunch and supper on the same day. 
            * **The Trend:** There is a moderate positive correlation (the red line goes up). This means that on days when lunch waste is high, supper waste also tends to be higher.
            * **The Implication:** This points to an overall "bad day" effect. This could mean our daily menu combinations are sometimes entirely unpopular, or perhaps overall student attendance in the dining hall drops on certain days (like Fridays). 
            """
        )
    
        return mo.vstack([question, graph, explanation])
    section_6_correlation(data)
    return


@app.cell
def _(alt, data, mo):
    def section_6_cumulative(df):
        # Calculate cumulative waste
        df_cum = df.copy()
        df_cum['Cumulative Total'] = (df_cum['lunch'] + df_cum['supper']).cumsum()
    
        # 1. The Question
        question = mo.md(
            """
            ---
            ## Question 7: How fast does the waste accumulate?
            Looking at daily numbers can sometimes hide the true magnitude of the problem. What does our waste look like as a running total?
            """
        )
    
        # 2. The Graph
        chart = alt.Chart(df_cum).mark_area(color='#2ca02c', opacity=0.6).encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Cumulative Total:Q', title='Total Accumulated Waste (kgs)'),
            tooltip=['date:T', 'Cumulative Total:Q']
        ).properties(
            width='container',
            height=350,
            title="Running Total of Food Waste"
        ).interactive()
    
        graph = mo.ui.altair_chart(chart)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ###  What this graph tells us:
            This area chart shows our running total of wasted food.
            * **The Steep Climb:** The curve is steep and relentless. In just 16 days, we reached almost **3,500 kg** of waste. 
            * **The Cost:** When we visualize the waste accumulating this quickly, it becomes clear how much budget is literally being thrown in the trash. If we project this trend out to an entire term, the numbers will be staggering.
            """
        )
    
        return mo.vstack([question, graph, explanation])
    section_6_cumulative(data)
    return


@app.cell
def _(alt, data, mo):
    def section_8_interactive_dashboard(df):
        # Prepare the data
        df_dash = df.copy()
        df_dash['Total Waste'] = df_dash['lunch'] + df_dash['supper']
        df_dash['Day'] = df_dash['date'].dt.day_name()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # 1. The Question
        question = mo.md(
            """
            ---
            ##  You can use this interractive dashboard to explore more patterns.
            Sometimes taking a step back and looking at the whole month is overwhelming.
            """
        )
    
        # 2. The Graph (Cross-Filtered Dashboard)
        # Create a 'brush' that allows the user to click and drag to select a range on the X-axis
        brush = alt.selection_interval(encodings=['x'])
    
        # Top Chart: The Timeline
        timeline = alt.Chart(df_dash).mark_area().encode(
            x=alt.X('date:T', title='Timeline (Click and drag to select a date range!)'),
            y=alt.Y('Total Waste:Q', title='Total Daily Waste'),
            # Gray out the area that is NOT selected by the brush
            color=alt.condition(brush, alt.value('#2ca02c'), alt.value('lightgray'))
        ).add_params(
            brush
        ).properties(
            width=500,
            height=200,
            title="Step 1: Click and drag your mouse over a section of this timeline"
        )
    
        # Bottom Chart: The Day of the Week breakdown (Updates based on the brush!)
        dow_bar = alt.Chart(df_dash).mark_bar().encode(
            x=alt.X('Day:N', sort=days, title='Day of the Week'),
            y=alt.Y('mean(Total Waste):Q', title='Average Waste'),
            color=alt.Color('Day:N', legend=None)
        ).transform_filter(
            brush # This tells the bottom chart to ONLY show data selected in the top chart
        ).properties(
            width=500,
            height=250,
            title="Step 2: Watch this weekly breakdown update based on your selection"
        )
    
        # Combine them vertically using Altair's '&' operator
        dashboard = timeline & dow_bar
    
        graph = mo.ui.altair_chart(dashboard)
    
        # 3. The Explanation
        explanation = mo.md(
            """
            ###  Try it yourself!
            This is a live dashboard. **Click and drag your mouse** across the top timeline to highlight a specific week. 
            * Notice how the bar chart below automatically recalculates the averages for only the days you selected?
            * You can drag the highlighted box left and right to "scrub" through the month and see how our weekly habits change over time!
            """
        )
    
        return mo.vstack([question, graph, explanation])

    section_8_interactive_dashboard(data)
    return


@app.cell
def _(mo):
    def section_9_acknowledgments():
        return mo.md(
            """
            ---
            ##  Acknowledgments & Thank You
        
            This presentation, and the insights we've gathered to help improve our school, would not have been possible without the generous support and cooperation of our dedicated staff.
        
            * **To Mr. Mangeni:** Thank you for championing this initiative and making the data collection process possible. 
            * **To the Entire Kitchen Department:** Thank you for your patience, hard work, and willingness to let us observe and track this data during your busy shifts.
            * **Special Shoutout to Asiimwe & Tinna:** We want to extend an extra special thank you to both of you for going above and beyond to help us in the kitchen while we were collecting this data. Your assistance was invaluable!
        
            <br>
        
            *Presented with gratitude by:*
            **The Science, Technology, and Innovation Club**
             *Kiira College Butiki*
            """
        )
    section_9_acknowledgments()
    return


@app.cell
def _(data, data_melted, mo):
    mo.md('Our dataset is here')
    data,data_melted
    return


if __name__ == "__main__":
    app.run()
