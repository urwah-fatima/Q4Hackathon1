// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive technical guide from perception to action',
  favicon: 'img/favicon.ico',

  // For Vercel deployment, use '/' as baseUrl
  // For GitHub Pages, change to '/humanoid-robotics-book/'
  url: process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : 'https://your-username.github.io',
  baseUrl: '/',

  organizationName: 'your-username',
  projectName: 'humanoid-robotics-book',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  markdown: {
    mermaid: false,
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        hideOnScroll: false,
        logo: {
          alt: 'Physical AI Book',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/your-username/humanoid-robotics-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {label: 'Module 1: ROS 2', to: '/module-1-ros2/ros2-architecture'},
              {label: 'Module 2: Simulation', to: '/module-2-simulation/gazebo-environment-setup'},
              {label: 'Module 3: Isaac', to: '/module-3-isaac/isaac-sim-synthetic-data'},
              {label: 'Module 4: VLA', to: '/module-4-vla/speech-to-command'},
            ],
          },
          {
            title: 'Resources',
            items: [
              {label: 'ROS 2 Docs', href: 'https://docs.ros.org/en/humble/'},
              {label: 'NVIDIA Isaac', href: 'https://developer.nvidia.com/isaac-sim'},
              {label: 'Gazebo', href: 'https://gazebosim.org/'},
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml', 'markup', 'json', 'csharp'],
      },
    }),
};

export default config;
