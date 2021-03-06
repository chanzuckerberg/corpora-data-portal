module.exports = {
  // (thuang): Prod build will serve static assets from this directory
  // E.g., cellxgene.cziscience.com/dp/foo.js
  assetPrefix: "/dp",
  plugins: [
    "gatsby-plugin-sass",
    "gatsby-plugin-typescript",
    "gatsby-plugin-react-helmet",
    "gatsby-plugin-root-import",
    "gatsby-plugin-styled-components",
    {
      resolve: "gatsby-plugin-asset-path",
    },
    {
      options: {
        name: `images`,
        path: `${__dirname}/src/common/images`,
      },
      resolve: `gatsby-source-filesystem`,
    },
    `gatsby-plugin-theme-ui`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      options: {
        crossOrigin: `use-credentials`,
        display: `minimal-ui`,
        icon: `src/common/images/cellxgene.png`, // This path is relative to the root of the site.
        name: `cellxgene`,
        short_name: `starter`,
        start_url: `/`,
      },
      resolve: `gatsby-plugin-manifest`,
    },
  ],
  siteMetadata: {
    author: `Chan Zuckerberg Initiative`,
    description: `
    The cellxgene data portal is a repository of public, explorable single-cell datasets.
    If you have a public dataset that you would like hosted on this site, please drop us a note at cellxgene@chanzuckerberg.com.
    `,
    title: `cellxgene`,
  },
};
