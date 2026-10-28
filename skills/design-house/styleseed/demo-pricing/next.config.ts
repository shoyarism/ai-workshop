import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // /motion-test was the dev slug; /motion is the canonical SEO route.
      { source: "/motion-test", destination: "/motion", permanent: true },
    ];
  },
};

export default nextConfig;
