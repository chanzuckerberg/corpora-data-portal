import React, { FC } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query-devtools";
import { isSSR } from "src/common/utils/isSSR";
import AppContainer from "src/components/AppContainer";
import CookieBanner from "src/components/CookieBanner";
import Layout from "../components/Layout";
import SEO from "../components/seo";

const queryClient = new QueryClient();

const Index: FC = () => {
  if (isSSR()) return null;

  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <SEO title="Explore Data" />
        <AppContainer />
        <CookieBanner />
      </Layout>
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
};

export default Index;
