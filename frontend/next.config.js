/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'www.dhm.de',
      },
      {
        protocol: "https",
        hostname: "kunstgraph.blob.core.windows.net",
        pathname: "/images/**"
      },
      {
        protocol: "https",
        hostname: "errproject.org",
        pathname: "/media/images/**"
      }
    ],
  },
};

module.exports = nextConfig;
