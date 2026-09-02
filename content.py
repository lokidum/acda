# -*- coding: utf-8 -*-
"""
Adelaide Confident Driving Academy — single source of truth.

Everything that a human might want to change lives here: business details,
pricing, reviews, suburbs, FAQs, page copy. build.py turns this into HTML.
Change a value here, run `python3 build.py`, redeploy.
"""

# ---------------------------------------------------------------------------
# Business constants
# ---------------------------------------------------------------------------

# TODO(loki): swap this for the live domain once it is registered, then re-run
# build.py. It is used for canonicals, Open Graph, sitemap.xml and JSON-LD.
SITE_URL = "https://adelaideconfidentdriving.com.au"

BRAND = "Adelaide Confident Driving Academy"
BRAND_SHORT = "Adelaide Confident Driving"
LEGAL_PREVIOUS = "Adelaide Driver Training Academy SA"
OLD_DOMAIN = "https://adelaidedrivertrainingacademysa.com.au"

INSTRUCTOR = "Gopi"
INSTRUCTOR_FULL = "Gopinathan"

PHONE_DISPLAY = "0423 457 296"
PHONE_TEL = "+61423457296"
WA_NUMBER = "61423457296"
EMAIL = "info@adelaideconfidentdriving.com.au"

RATING = "5.0"
REVIEW_COUNT = 72

GOOGLE_PROFILE = "https://share.google/oz1qiCDrlBlNMlHzZ"
GOOGLE_KG = "https://www.google.com/search?kgmid=/g/11vqnhx90x"

FOUNDED = "1990"
HOURS_TEXT = "Monday to Sunday, closes 8:00pm"

REGION = "South Australia"
LOCALITY = "Adelaide"
POSTAL_REGION = "SA"
GEO_LAT = "-34.9285"
GEO_LNG = "138.6007"
SERVICE_RADIUS_KM = "40"

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

NAV = [
    ("Lessons", "/services/"),
    ("Pricing", "/pricing/"),
    ("About Gopi", "/about/"),
    ("Reviews", "/reviews/"),
    ("Areas", "/service-areas/"),
    ("FAQ", "/faq/"),
    ("Contact", "/contact/"),
]

# ---------------------------------------------------------------------------
# Service areas
# ---------------------------------------------------------------------------

AREAS = [
    {
        "name": "Adelaide CBD and inner suburbs",
        "slug": "cbd",
        "blurb": "Tight one-way grids, tram lines, cyclists and constant lane changes. "
                 "Inner Adelaide is where most learners lose marks, so it is where most "
                 "of the training time goes.",
        "suburbs": ["Adelaide CBD", "North Adelaide", "Norwood", "Unley", "Prospect",
                    "Parkside", "Hindmarsh", "Thebarton", "Kent Town", "Goodwood"],
    },
    {
        "name": "Northern suburbs",
        "slug": "north",
        "blurb": "Wide arterials, high speed limits and long merges. Good ground for "
                 "building confidence early, and for practising the road positioning "
                 "the test actually scores.",
        "suburbs": ["Salisbury", "Elizabeth", "Mawson Lakes", "Para Hills", "Gepps Cross",
                    "Pooraka", "Ingle Farm", "Modbury", "Golden Grove", "Munno Para"],
    },
    {
        "name": "Western suburbs",
        "slug": "west",
        "blurb": "Port Road, heavy freight traffic and a lot of unmarked intersections "
                 "through the older street grids. Excellent for hazard perception practice.",
        "suburbs": ["Port Adelaide", "Woodville", "Henley Beach", "Findon", "Seaton",
                    "West Lakes", "Fulham", "Grange", "Semaphore", "Royal Park"],
    },
    {
        "name": "Eastern suburbs",
        "slug": "east",
        "blurb": "Hills approaches, gradients, roundabouts and some genuinely awkward "
                 "give-way geometry. Where hill starts and downhill control get sorted.",
        "suburbs": ["Campbelltown", "Tea Tree Gully", "Magill", "Athelstone", "Paradise",
                    "Newton", "Rostrevor", "Burnside", "Glen Osmond", "Hectorville"],
    },
]

SOUTHERN_NOTE = (
    "Southern suburbs including Marion, Mitcham, Morphett Vale, Brighton and Noarlunga "
    "can be arranged on request. Send a message and Gopi will let you know what is "
    "workable around his current schedule."
)

# Chips shown under the suburb field in the booking widget
SUBURB_CHIPS = ["Adelaide CBD", "Salisbury", "Mawson Lakes", "Norwood",
                "Port Adelaide", "Campbelltown", "Modbury", "Prospect"]

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

SERVICES = [
    {
        "slug": "cbta-logbook-training",
        "nav": "CBT&A logbook training",
        "title": "CBT&A Driving Lessons Adelaide | Logbook Method",
        "h1": "CBT&A logbook training in Adelaide",
        "meta": "CBT&A driving lessons across Adelaide with Gopi. 30 logbook tasks signed off as you go, no pass or fail final test. 5.0 stars from 72 reviews.",
        "tagline": "Thirty tasks, signed off as you go. No single test day deciding everything.",
        "keyword": "CBT&A Adelaide",
        "icon": "logbook",
        "chip": "Most popular",
        "summary": "Competency Based Training and Assessment. Your Authorised Examiner "
                   "signs off each task as you demonstrate it, so there is no pass or fail "
                   "moment at the end.",
        "intro": [
            "CBT&A stands for Competency Based Training and Assessment. Instead of building "
            "up to one high-pressure test, you work through the 30 tasks set out in your "
            "Driving Companion, and your Authorised Examiner records each one as you "
            "demonstrate it competently.",
            "For a lot of learners this is the difference between passing and not. Test-day "
            "nerves are real, and a single bad morning can cost you months. The logbook "
            "method removes that cliff edge entirely.",
        ],
        "benefits": [
            ("There is no pass or fail", "You are assessed task by task. Nothing hinges on "
             "one morning and one examiner."),
            ("You set the pace", "No test deadline forcing you into the car before you are "
             "ready, and no artificial rush through the tasks you find hardest."),
            ("Re-training happens on the spot", "If a task is not signed off, Gopi re-trains "
             "you and re-assesses it in the same lesson or the next one. There is no 14 day "
             "wait like a failed VORT."),
            ("It builds actual driving habits", "The 30 tasks are designed around good "
             "driving behaviour, not test tricks. You come out of it a better driver, which "
             "matters more than the licence."),
        ],
        "process": [
            ("Assessment drive", "A first lesson to see where you actually are. Gopi maps "
             "which of the 30 tasks you can already demonstrate and which need work."),
            ("Structured task work", "Lessons target specific competencies rather than "
             "wandering around aimlessly. Slow-speed manoeuvres, hazard perception, road "
             "positioning, and the decision-making that examiners watch closest."),
            ("Progressive sign-off", "Each task gets recorded on your form as you nail it. "
             "You can see the logbook filling up, which does more for confidence than any "
             "pep talk."),
            ("The final drive", "A consolidation drive covering everything, and your "
             "paperwork completed. Then you are done."),
        ],
        "faqs": [
            ("How long does CBT&A take in Adelaide?",
             "It depends entirely on where you start. Someone with a lot of supervised hours "
             "behind them might complete the 30 tasks in a handful of lessons. A genuine "
             "beginner should expect considerably more. Gopi gives you a realistic estimate "
             "after the first assessment drive rather than quoting a number that sounds good "
             "on a website."),
            ("Do I still need to log 75 hours if I do CBT&A?",
             "No. The 75 hour supervised driving requirement applies to the VORT pathway. "
             "CBT&A learners work through the competency tasks instead. Check your current "
             "conditions on mylicence.sa.gov.au, since requirements do change."),
            ("Can I switch from VORT to CBT&A?",
             "Yes. Plenty of people come across after a failed VORT, or after realising that "
             "a single timed test is not how they perform best. Nothing you have already done "
             "is wasted."),
            ("Is CBT&A available for overseas licence holders?",
             "Yes, and it is the pathway most overseas drivers choose. See the overseas "
             "licence conversion page for how that works."),
        ],
        "price_group": "cbta",
    },
    {
        "slug": "vort-test-preparation",
        "nav": "VORT test preparation",
        "title": "VORT Test Preparation Adelaide | Mock Tests",
        "h1": "VORT test preparation in Adelaide",
        "meta": "VORT preparation, mock tests and test day bookings across Adelaide. The five slow-speed manoeuvres drilled properly, plus the instant-fail list.",
        "tagline": "Ninety percent is the pass mark and one road law breach ends the drive. Preparation is not optional.",
        "keyword": "VORT test Adelaide",
        "icon": "target",
        "chip": "Test ready",
        "summary": "Vehicle On Road Test drills, honest mock assessments, and test day "
                   "bookings in your car or the instructor's.",
        "intro": [
            "The Vehicle On Road Test is the other route to a P1 provisional licence. You "
            "record 75 hours of supervised driving, then sit a single assessed drive.",
            "Here is the part people underestimate: 75 logged hours with a parent or partner "
            "does not mean you are prepared for the VORT. You have to demonstrate five "
            "slow-speed manoeuvres, score 90 percent or better across the general drive, and "
            "not breach road law once. Any breach and the test is terminated on the spot. "
            "Hours in the seat and readiness for the assessment are two different things.",
        ],
        "benefits": [
            ("The five manoeuvres, drilled",
             "Move off, angle park, U-turn, three point turn and reverse parallel park. These "
             "get practised until they are boring, because boring is what passing looks like."),
            ("An honest mock test",
             "A mock assessment run the way the real one is run, marked the way the real one "
             "is marked. If you are not ready, you find out from Gopi rather than from an "
             "examiner."),
            ("The instant-fail list",
             "Most VORT failures are not sloppy parking. They are a missed give-way, a "
             "creeping stop line, or a lane change without a head check. You get told exactly "
             "where those live on Adelaide roads."),
            ("Test day in a car you know",
             "Sit the test in your own roadworthy vehicle, or use Gopi's with an hour of "
             "practice beforehand so nothing about the car is a surprise."),
        ],
        "process": [
            ("Pre-VORT lesson", "A 60 minute session that finds the gaps. Usually not where "
             "people expect them to be."),
            ("Targeted drills", "Whichever manoeuvres and road situations came out weakest, "
             "worked until they are automatic rather than hopeful."),
            ("Mock test", "A full simulated assessment with a marking sheet, so the real one "
             "is a repeat rather than a first."),
            ("Test day", "Booked in your vehicle or Gopi's, with a practice drive first if "
             "you are using his."),
        ],
        "faqs": [
            ("What happens if I fail my VORT?",
             "Your examiner debriefs you on why, and you get a copy of the marking sheet "
             "detailing your performance. If you hold a learner's permit you must wait at "
             "least 14 days before attempting another VORT."),
            ("What is the VORT pass mark?",
             "You need 90 percent or more across the general drive, plus successful "
             "demonstration of the five slow-speed manoeuvres, and no road law breaches. A "
             "breach terminates the test immediately regardless of how well the rest went."),
            ("Can I use my own car for the VORT?",
             "Yes, provided it is roadworthy and meets the requirements. Gopi will tell you "
             "what gets checked before you turn up, because being turned away for a "
             "mechanical issue is a miserable way to lose a booking."),
            ("How many lessons before I book the test?",
             "Book the mock test first. It answers the question far better than a guess does."),
        ],
        "price_group": "vort",
    },
    {
        "slug": "overseas-licence-conversion",
        "nav": "Overseas licence conversion",
        "title": "Overseas Licence Conversion Adelaide | Full SA Licence",
        "h1": "Overseas licence conversion in Adelaide",
        "meta": "Convert your overseas driver licence to a full South Australian licence. CBT&A pathway built around SA road law for experienced international drivers.",
        "tagline": "You can already drive. This is about how South Australia expects it done.",
        "keyword": "overseas licence conversion Adelaide",
        "icon": "globe",
        "chip": "Fast tracked",
        "summary": "For experienced drivers converting an international licence. Built "
                   "around SA road law and the local habits that catch people out.",
        "intro": [
            "If you have been driving for years overseas, being treated like a total beginner "
            "is both insulting and a waste of your money. The conversion process is not about "
            "teaching you to drive. It is about the gap between how you learned and how South "
            "Australia assesses.",
            "That gap is usually smaller than people fear and more specific than they expect. "
            "Roundabout signalling, give-way rules at unmarked intersections, the head check "
            "requirement, speed tolerance, and the way examiners score road positioning. Sort "
            "those and the rest follows.",
        ],
        "benefits": [
            ("Assessed on what you can already do",
             "The first drive establishes your actual level. Nobody sits through lessons on "
             "how to use a steering wheel."),
            ("SA-specific road law",
             "Give-way rules, roundabout signalling, school zones, and the local conventions "
             "that are not written anywhere but get marked anyway."),
            ("CBT&A pathway, no final exam",
             "Most overseas drivers take the logbook route. Tasks get signed off as you "
             "demonstrate them, which suits experienced drivers well."),
            ("Patient with language and nerves",
             "Instructions are explained in plain terms and repeated as often as needed. "
             "Several of the reviews on this site come from drivers who converted with Gopi."),
        ],
        "process": [
            ("Where you actually stand", "One drive to assess your existing skill and identify "
             "the SA-specific gaps."),
            ("Road law and local conventions", "The rules that differ from where you learned, "
             "taught in context rather than from a book."),
            ("Task sign-offs", "Working through the CBT&A competencies at a pace that "
             "respects your experience."),
            ("Full SA licence", "Paperwork completed and you are driving on your own licence."),
        ],
        "faqs": [
            ("Which countries can convert without a test?",
             "It depends on your country of issue and your licence class. Some are recognised "
             "for direct conversion, others require assessment. Service SA publishes the "
             "current list, and Gopi can talk you through where you sit before you book "
             "anything."),
            ("How long do I have to convert after arriving?",
             "There are timeframes attached to overseas licences in South Australia and they "
             "vary with your visa status. Check mylicence.sa.gov.au for your situation, "
             "because getting this wrong can leave you driving unlicensed without realising."),
            ("Do I need to do the full 30 CBT&A tasks?",
             "You work through the competencies, but an experienced driver typically moves "
             "through them considerably faster than a first-time learner."),
            ("Can I do this in an automatic?",
             "Yes. Note that if you are assessed in an automatic, your SA licence carries an "
             "automatic-only condition."),
        ],
        "price_group": "cbta",
    },
    {
        "slug": "beginner-driving-lessons",
        "nav": "Beginner and nervous drivers",
        "title": "Nervous Driver Lessons Adelaide | Patient Instructor",
        "h1": "Beginner and nervous driver lessons",
        "meta": "Calm, patient driving lessons in Adelaide for absolute beginners and anxious drivers. Quiet streets first, no shouting, no rushing. 5.0 stars.",
        "tagline": "Quiet streets first. Nobody is going to shout at you.",
        "keyword": "nervous driver lessons Adelaide",
        "icon": "heart",
        "chip": "Anxiety friendly",
        "summary": "For first-timers and anyone who has had a bad experience with an "
                   "instructor. Slow start, quiet roads, and a pace set by you.",
        "intro": [
            "Some people take to driving straight away. Plenty of others find it genuinely "
            "frightening, and being told to relax has never once helped anybody relax.",
            "This is the part of the job Gopi is best known for. Look at the reviews and the "
            "same word keeps coming up: patient. One learner did her lessons while nine months "
            "pregnant. Another had been through several instructors before finding one who "
            "explained things properly. The method is not complicated, it is just applied "
            "consistently: start quiet, explain before doing, and never move on until the "
            "current thing feels manageable.",
        ],
        "benefits": [
            ("Quiet streets to begin with",
             "The first lesson is not on Port Road. Empty back streets, low stakes, and time "
             "to get used to the car itself."),
            ("Explained before attempted",
             "Every manoeuvre gets broken down and talked through before you are asked to do "
             "it. Reviewers mention this specifically and often."),
            ("No shouting, no sighing",
             "Thirty years in and Gopi has seen every mistake there is. None of them are "
             "worth raising your voice over."),
            ("Your pace, not a schedule",
             "If a lesson needs to be spent on one intersection until it stops being scary, "
             "that is what the lesson is spent on."),
        ],
        "process": [
            ("Sitting in the car", "Controls, mirrors, seat position, and what everything "
             "does. Sounds basic. It is the foundation for everything after it."),
            ("Quiet street driving", "Moving off, stopping, steering and gear changes with "
             "nothing much around you."),
            ("Building the road picture", "Traffic, intersections, roundabouts and lane "
             "changes, introduced one at a time as you are ready."),
            ("Choosing a pathway", "Once driving feels normal, you and Gopi decide whether "
             "CBT&A or the VORT suits you better."),
        ],
        "faqs": [
            ("I am scared of driving. Is that a problem?",
             "It is extremely common and it is not a problem. Say so at the start of the first "
             "lesson and the pace gets set accordingly. Nothing gets sprung on you."),
            ("I had a bad experience with another instructor.",
             "Also common, unfortunately. Several of the reviews on this site are from people "
             "who came across after that exact situation."),
            ("Should I learn in an automatic or a manual?",
             "If you are anxious, automatic removes a whole layer of things to think about, "
             "and it is what most learners choose now. The trade-off is that an automatic-only "
             "licence restricts what you can legally drive later."),
            ("What if I need extra time on something?",
             "Then you get extra time on it. That is the entire point of one-to-one lessons."),
        ],
        "price_group": "cbta",
    },
    {
        "slug": "refresher-driving-lessons",
        "nav": "Refresher lessons",
        "title": "Refresher Driving Lessons Adelaide | Get Confident",
        "h1": "Refresher driving lessons in Adelaide",
        "meta": "Refresher driving lessons in Adelaide for licenced drivers returning after a break, an incident, or years off the road. Calm and judgement free.",
        "tagline": "You have the licence. Getting the confidence back is a different job.",
        "keyword": "refresher driving lessons Adelaide",
        "icon": "refresh",
        "chip": "No judgement",
        "summary": "For licenced drivers who have been off the road, lost their nerve, or "
                   "want to sharpen up before a big drive.",
        "intro": [
            "Holding a licence and feeling capable behind the wheel are not the same thing. "
            "People come back to driving after years away, after a crash, after moving from a "
            "country town to a city, or after a long stretch where somebody else always drove.",
            "There is nothing embarrassing about any of that, and a refresher lesson is a "
            "considerably cheaper way to deal with it than the alternative.",
        ],
        "benefits": [
            ("Start wherever you need to",
             "Some people want a quiet-streets reset. Others want to go straight at the "
             "freeway merge that has been bothering them."),
            ("Specific problems, specifically fixed",
             "Reverse parking, roundabouts, night driving, motorways, hills. Bring the thing "
             "you avoid and work on it directly."),
            ("Zero judgement",
             "Nobody is going to make you feel foolish for being out of practice."),
            ("Useful before a big change",
             "Worth doing before a long road trip, a move to a busier area, or going back to "
             "driving for work."),
        ],
        "process": [
            ("A conversation first", "What has changed, what worries you, and what you want "
             "out of it."),
            ("An honest assessment drive", "Where your driving actually is now, said plainly."),
            ("Focused practice", "Time spent on the specific things that need it."),
            ("Back to it", "As many or as few sessions as it takes. Most people need fewer "
             "than they expect."),
        ],
        "faqs": [
            ("How many refresher lessons will I need?",
             "Often one or two. Sometimes more if it has been a very long break. You will get "
             "a straight answer after the first drive rather than a package sold to you upfront."),
            ("I have not driven in ten years. Is that too long?",
             "No. It comes back faster than you would think, especially with someone calm in "
             "the passenger seat."),
            ("Can I use my own car?",
             "Yes, as long as it is roadworthy and appropriately insured. For some people "
             "that is exactly the right call, since the car is part of what feels unfamiliar."),
            ("I had an accident and I am nervous now.",
             "Very understandable, and a common reason people book. The pace is yours to set."),
        ],
        "price_group": "cbta",
    },
]

# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------
# TODO(loki): confirm every figure with Gopi before launch. These are carried
# across from adelaidedrivertrainingacademysa.com.au as at September 2026.

PRICE_DISCLAIMER = (
    "All prices are indicative starting points in Australian dollars and are current as at "
    "September 2026. Final pricing depends on your location, lesson length and how many "
    "sessions you need. Send a message for a firm quote before you book."
)

PRICING = {
    "cbta": {
        "label": "CBT&A logbook training",
        "note": "Competency Based Training and Assessment. Tasks signed off as you go.",
        "items": [
            {"name": "90 minute lesson", "dur": "90 minutes", "price": "180",
             "desc": "The standard lesson length. Long enough to cover real ground without "
                     "losing concentration.", "featured": False},
            {"name": "120 minute lesson", "dur": "120 minutes", "price": "230",
             "desc": "Better value per minute, and useful when you are working through "
                     "several tasks in one go.", "featured": False},
            {"name": "10 lesson package", "dur": "10 x 90 minutes", "price": "1700",
             "desc": "Works out cheaper than booking singles and gives you a clear run at "
                     "the full task list.", "featured": True},
            {"name": "The final drive", "dur": "Includes pre-drive", "price": "330",
             "desc": "Consolidation drive and completion of your paperwork.", "featured": False},
        ],
    },
    "vort": {
        "label": "VORT test preparation",
        "note": "Vehicle On Road Test drills, mock assessments and test day bookings.",
        "items": [
            {"name": "Pre-VORT lesson", "dur": "60 minutes", "price": "110",
             "desc": "Targeted preparation for the test. The usual starting point.",
             "featured": False},
            {"name": "VORT mock test", "dur": "60 minutes", "price": "110",
             "desc": "A full simulated assessment so you know whether you are actually ready.",
             "featured": True},
            {"name": "3 lesson VORT pack", "dur": "180 minutes total", "price": "320",
             "desc": "Solid preparation for most learners who have their hours logged.",
             "featured": False},
            {"name": "5 lesson VORT pack", "dur": "300 minutes total", "price": "525",
             "desc": "Thorough preparation with room to drill weak manoeuvres properly.",
             "featured": False},
            {"name": "VORT test, your vehicle", "dur": "60 minutes", "price": "250",
             "desc": "An examiner conducts your test in your own car. Vehicle must be roadworthy.",
             "featured": False},
            {"name": "VORT test, instructor vehicle", "dur": "120 minutes", "price": "425",
             "desc": "An hour of practice in the instructor's car, then the examiner conducts "
                     "your test in it.", "featured": False},
        ],
    },
}

# ---------------------------------------------------------------------------
# Reviews (verbatim from the Google Business Profile)
# ---------------------------------------------------------------------------

REVIEW_TAGS = [
    ("all", "All reviews"),
    ("first-attempt", "First attempt pass"),
    ("cbta", "CBT&A"),
    ("vort", "VORT prep"),
    ("overseas", "Overseas conversion"),
    ("patience", "Patient instruction"),
]

REVIEWS = [
    {"name": "Basil Eldhose", "tag": "First attempt pass", "tags": ["first-attempt", "patience"],
     "text": "I had a great experience learning with Gopi. He is very patient, friendly, and "
             "explains everything in a simple way. His guidance helped me build confidence and "
             "pass my driving test on the first attempt."},
    {"name": "Zandy", "tag": "Best in Adelaide", "tags": ["patience"],
     "text": "Absolutely the best instructor in Adelaide, I know this because I have had many "
             "instructors before him. He really works hard to make sure you succeed, excellent "
             "teaching ability, and a positive attitude."},
    {"name": "Mina Prajapat", "tag": "Patience and support", "tags": ["patience"],
     "text": "I can't thank Gopi Sir enough for all the support and patience he showed during "
             "my driving lessons, especially while I was in my 9th month of pregnancy. His calm "
             "demeanor and clear guidance made it possible."},
    {"name": "Chinthika Samarakoon", "tag": "Overseas conversion", "tags": ["overseas", "cbta", "patience"],
     "text": "I did my overseas licence conversion through CBT&A with Gopi and got the full SA "
             "driver's licence. Gopi was an excellent teacher, kind, respectful, and patient "
             "throughout the entire process."},
    {"name": "Vedant Saini", "tag": "CBT&A success", "tags": ["cbta", "first-attempt"],
     "text": "Excellent instructor! Gopi really knows his stuff. Lots of tips and tricks which "
             "got my confidence up. Passed my CBT&A with an Auditor in the car on the first try!"},
    {"name": "Xander Schofield", "tag": "VORT preparation", "tags": ["vort"],
     "text": "Gopi was incredibly helpful in getting my P's. In the session right before the "
             "exam, he helped correct mistakes quickly and efficiently."},
    {"name": "Anh Quang Le Van", "tag": "Rapid completion", "tags": ["first-attempt", "patience"],
     "text": "Experienced, gentle, and patient enough to help me pass the full license test in "
             "just 2 training sessions. He organized early timeframes for my urgent timeline."},
    {"name": "Aishwarya Menon", "tag": "First attempt pass", "tags": ["first-attempt", "patience"],
     "text": "I passed my driving test the first time! Gopi uncle broke down each task and "
             "ensured I understood the movement prior to attempting it on the road."},
]

# ---------------------------------------------------------------------------
# Site-wide FAQ
# ---------------------------------------------------------------------------

FAQS = [
    ("What is the difference between CBT&A and the VORT?",
     "CBT&A is the logbook method. You work through 30 competency tasks and your Authorised "
     "Examiner signs each one off as you demonstrate it, so there is no pass or fail moment. "
     "The VORT is a single assessed drive after 75 logged supervised hours, where you need 90 "
     "percent or better and no road law breaches. CBT&A suits people who do not perform well "
     "under test pressure. The VORT suits confident drivers who would rather get it done in "
     "one sitting."),
    ("Do you teach automatic or manual?",
     "Both. Most learners now choose automatic, which is completely reasonable. Be aware that "
     "if you are assessed in an automatic, your licence carries an automatic-only condition "
     "until you complete a manual assessment."),
    ("Which parts of Adelaide do you cover?",
     "The CBD and inner suburbs, the northern suburbs, the western suburbs and the eastern "
     "suburbs. Southern suburbs can be arranged on request depending on the schedule. Send a "
     "message with your suburb and you will get a straight answer."),
    ("Can you pick me up from home, work or uni?",
     "Usually yes, within the service areas. Say where you need to be picked up from when you "
     "message and it gets sorted before the first lesson."),
    ("How many lessons will I need?",
     "Nobody can answer that honestly before seeing you drive. After the first assessment "
     "lesson you will get a realistic estimate rather than a number designed to sound "
     "appealing."),
    ("How do I book?",
     "The quickest way is the WhatsApp booking form on this site, which sends Gopi your "
     "training path, transmission, suburb and preferred timing in one message. Calling or "
     "texting " + PHONE_DISPLAY + " works just as well."),
    ("What are your hours?",
     "Seven days a week, closing at 8:00pm. Early morning and evening slots are often "
     "available, which helps if you are working or studying full time."),
    ("Are you the same business as Adelaide Driver Training Academy SA?",
     "Yes. Adelaide Confident Driving Academy is the new trading name for Adelaide Driver "
     "Training Academy SA. Same instructor, same experience, same phone number. Only the name "
     "and the website have changed."),
    ("How much do driving lessons cost in Adelaide?",
     "Indicative pricing is published on the pricing page rather than hidden behind an "
     "enquiry form. CBT&A lessons start from $180 for 90 minutes and VORT preparation from "
     "$110 for 60 minutes. Final pricing depends on your location and how many sessions you "
     "need."),
    ("Do you help with the hazard perception test or the theory test?",
     "Those are done online through Service SA, but Gopi can point you at the right practice "
     "resources and talk through the parts people commonly get wrong. The official links are "
     "in the footer of every page."),
]

# ---------------------------------------------------------------------------
# Instructor
# ---------------------------------------------------------------------------

INSTRUCTOR_BIO = [
    "Gopi has been teaching people to drive in South Australia since 1990. Before that, and "
    "alongside it, his background is in automobile engineering, which is a longer way of "
    "saying he understands what the car is doing as well as what the driver is doing.",
    "Over three decades that adds up to a lot of learners. Nervous seventeen year olds. "
    "Overseas drivers with twenty years of experience in a different road system. People "
    "coming back after a decade off. Someone doing her lessons in the ninth month of "
    "pregnancy. The approach does not change much between them: work out where the person "
    "actually is, explain things before asking them to be done, and do not move on until the "
    "current thing feels manageable.",
    "Every lesson is one to one. There is no rotating roster of instructors and no shared "
    "sessions. You get the same person every time, which matters more than most driving "
    "schools admit, because half of learning to drive is trusting the voice in the passenger "
    "seat.",
    "The business traded as Adelaide Driver Training Academy SA for many years. The name "
    "changed to Adelaide Confident Driving Academy because confidence, not just competence, is "
    "the thing people actually come here for. Everything else about it is the same.",
]

CREDENTIALS = [
    ("Teaching since 1990", "More than 30 years of driver training in South Australia."),
    ("Automobile engineering background", "A mechanical understanding of the vehicle, not "
     "just the road rules."),
    ("Authorised Examiner for CBT&A", "Able to assess and sign off the 30 competency tasks "
     "directly."),
    ("5.0 stars from 72 Google reviews", "Not a single review below five stars at the time of "
     "writing."),
    ("One-to-one instruction only", "The same instructor every lesson, with training adapted "
     "to how you learn."),
    ("Automatic and manual", "Both transmissions taught and assessed."),
]

# Photo slots the client fills in later. Drop files at these paths and the
# placeholders are replaced automatically on the next build.
PHOTOS = {
    "hero": {"file": "gopi-portrait.jpg", "alt": "Gopi, lead driving instructor at Adelaide Confident Driving Academy"},
    "strip": [
        {"file": "gopi-car-1.jpg", "alt": "Gopi with the Adelaide Confident Driving Academy training vehicle"},
        {"file": "gopi-lesson-1.jpg", "alt": "A driving lesson in progress on an Adelaide street"},
        {"file": "gopi-student-pass.jpg", "alt": "A student celebrating a first attempt pass"},
    ],
}

# ---------------------------------------------------------------------------
# Official resources
# ---------------------------------------------------------------------------

RESOURCES = [
    ("The Driving Companion", "https://mylicence.sa.gov.au/the-driving-companion"),
    ("The Driver's Handbook", "https://mylicence.sa.gov.au/the-drivers-handbook"),
    ("Hazard Perception Test practice", "https://mylicence.sa.gov.au/hazard-perception-test"),
    ("RAA driving tests and services", "https://www.raa.com.au/motoring-and-road-safety/driver-education"),
]

ACKNOWLEDGEMENT = (
    "Adelaide Confident Driving Academy acknowledges we are on the traditional Country of the "
    "Kaurna people of the Adelaide Plains and pays respect to Elders past, present and "
    "emerging. We recognise and respect their cultural heritage, beliefs and relationship with "
    "the land. We also extend that respect to visitors of other Aboriginal language groups and "
    "other First Nations."
)
