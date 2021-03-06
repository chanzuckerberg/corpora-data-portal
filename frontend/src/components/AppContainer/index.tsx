import loadable from "@loadable/component";
import { RouteComponentProps, Router } from "@reach/router";
import React, { FC } from "react";
import { ROUTES } from "src/common/constants/routes";
import { Props } from "src/views/Collection";

const AsyncHomepage = loadable<RouteComponentProps>(
  () => /*webpackChunkName: 'Homepage' */ import("src/views/Homepage")
);

const AsyncMyCollections = loadable<RouteComponentProps>(
  () =>
    /*webpackChunkName: 'AsyncMyCollections' */ import(
      "src/views/MyCollections"
    )
);

const AsyncCollection = loadable<Props>(
  () => /*webpackChunkName: 'AsyncCollection' */ import("src/views/Collection")
);

const AppContainer: FC = () => {
  return (
    <Router>
      <AsyncHomepage path={ROUTES.HOMEPAGE} />
      <AsyncMyCollections path={ROUTES.MY_COLLECTIONS} />
      <AsyncCollection path={ROUTES.COLLECTION} />
      <AsyncCollection path={ROUTES.PRIVATE_COLLECTION} />
    </Router>
  );
};

export default AppContainer;
