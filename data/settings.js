const me = {
    name: 'Carlos',
    surname: ['Fernández', 'Llamas'],
    get fullName() { return `${me.name} ${me.surname.join(' ')}` },
    alias: 'Sirikon'
};

const job = {
    get currentPosition() { return job.positions[0] },
    positions: [
        {
            role: 'Full Stack Engineer',
            company: {
                name: 'Lookiero',
                url: 'https://lookiero.es/'
            },
            since: 'August 2019',
            until: 'Today',
            text: []
        },
        {
            role: 'Software Developer',
            company: {
                name: 'Plain Concepts',
                url: 'https://www.plainconcepts.com/',
            },
            since: 'September 2015',
            until: 'August 2019',
            text: [
                'Development, consulting and training role in the Bilbao office of Plain Concepts for multiple clients in many industries, both brand new and legacy projects.',
                'In charge of development of many solutions, using the latest technologies available that suit with the project\'s requirements.',
                'Working mostly with .NET Technologies, Azure Cloud, Web Technologies, Containers and Container Orchestration.',
                'Also some experimentation with stuff like Microsoft Band, UWP and Xamarin.'
            ]
        },
        {
            role: 'I+D+i Project Manager',
            company: {
                name: 'Seis Cocos',
                url: 'http://seiscocos.com/'
            },
            since: 'May 2013',
            until: 'June 2015',
            text: [
                'Responsible of every project that requires cutting-edge web technologies, responsible of internal tools and frameworks development, main software architect and systems/services maintainer.',
                'I accomplished great look&feel, functionality and stability in much lower time than other environments by using web technologies, this way the application was automatically multiplatform, saving time and money.',
                'Most of the time, PHP, Node, Cordova, MySQL and MongoDB were involved, while dealing with On-Premise infrastructure.',
                'Helped in game development with Unity Engine and developed an unreleased tamagotchi-like game for Samsung Galaxy Gear (Tizen).'
            ]
        },
        {
            role: 'Intern',
            company: {
                name: 'Ichton Software',
                url: 'https://es.linkedin.com/company/ichton-software-s.l.'
            },
            since: 'February 2013',
            until: 'June 2013',
            text: [
                'Made some web pages for clients and helped in other areas.',
                'Mostly computer repair, WordPress installation, configuration and theme customization, and some static pages with plain HTML and CSS.'
            ]
        }
    ]
};

module.exports = {
    data() {
        return {
            title: 'Sirikon.me',
            description: `${me.fullName} personal website.`,
            url: process.env.SIRIKONME_URL || 'http://localhost:3000',
            footer: `${me.alias}.me - 2020`,

            me,

            about: {
                facts: [
                    ["Born in", "Málaga, Andalusia", "https://www.openstreetmap.org/relation/340746"],
                    ["Living in", "Bilbao, Basque Country", "https://www.openstreetmap.org/relation/339549"],
                    ["Working on", job.currentPosition.company.name, job.currentPosition.company.url],
                    ["Mostly", "programming", "https://github.com/sirikon/"],
                    ["Even some", "games", "https://sirikon.itch.io/"],
                    ["Doing some", "photography", "https://500px.com/sirikon"],
                    ["Talking on", "the fediverse", "https://plaza.remolino.town/sirikon"],
                ],
                contact: [
                    ["Email", "hello@sirikon.me", "mailto:hello@sirikon.me"],
                    ["ActivityPub", "@sirikon@plaza.remolino.town", "https://plaza.remolino.town/sirikon"],
                ]
            },

            job,
        }
    }
}
