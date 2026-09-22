# PinkyDS — On women killing in this country

A data-analysis project on femicide in Italy, built around a simple, uncomfortable idea:
**data doesn't lie, but people do.** The same numbers, sliced from different angles, can be
made to tell opposite stories. This project takes real data from the Italian National
Institute of Statistics (ISTAT) and shows how easily it can be twisted to support a
convenient narrative and then undoes each distortion to show what the data actually says.

It was built as a personal project, prompted by a series of misleading public claims about
femicide, to demonstrate how statistics get misused in public debate.

🔗 **Live app:** https://pinky-ds.onrender.com/
*(hosted on a free tier — it may take ~30 seconds to wake up on first load)*

## The idea

Each section presents a claim the way someone might weaponize the data to make it, then
takes it apart. The point is not that "data can prove anything," but the opposite: that
reading data honestly requires resisting the easy, agenda-driven angle.

## The three stories

**1. "There's no issue — men die more."**
True in raw counts: from 2002 to 2023, men are the majority of homicide victims in Italy.
But the aggregate hides the structure. Break the numbers down by who did the killing, and
the picture inverts: for women, the largest share of killers are partners and ex-partners,
people they lived with and trusted. For men, that share is negligible. The same dataset,
disaggregated, tells a completely different story.
*(A lesson in how aggregate figures conceal the actual phenomenon.)*

**2. "The North is more dangerous."**
48% of femicides happened in the North almost half. Case closed, if you stop at the
headline. But normalize by population, and the map flips: proportionally, the danger shifts
toward the South, the islands, and smaller regions. The North doesn't have more violence,
it has more people.
*(A lesson in raw counts vs. per-capita rates.)*

**3. "Illegal migration drives gender violence."**
A claim that's headline-ready and impossible to check because in Italy there is no data
on the citizenship or migration status of people who commit gender based violence. You can't
debunk it, because the data to debunk it was never collected. The absence of data becomes its
own form of manipulation: an unfalsifiable claim protected by a gap in the record.
*(A lesson in how missing data enables claims that can't be tested.)*

## Data source

Data from the Italian National Institute of Statistics (ISTAT).

## Built with

Python, Dash, Plotly, pandas

## Running locally

```bash
git clone https://github.com/Carbai/pinky_ds.git
cd pinky_ds
pip install -r requirements.txt
python app.py
```
