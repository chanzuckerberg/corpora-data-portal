import { AnchorButton, Button, Classes, Intent } from "@blueprintjs/core";
import React, { FC } from "react";
import { API } from "src/common/API";
import { QUERY_PARAMETERS } from "src/common/constants/queryParameters";
import { API_URL } from "src/configs/configs";
import { ContentWrapper } from "./style";

interface Props {
  onClose: () => void;
}

const CTA: FC<Props> = ({ onClose }) => {
  return (
    <>
      <ContentWrapper>
        Only registered users can create collections.
      </ContentWrapper>
      <Footer />
    </>
  );

  function Footer() {
    return (
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button minimal intent={Intent.PRIMARY} onClick={onClose}>
            Cancel
          </Button>
          <AnchorButton
            intent={Intent.PRIMARY}
            href={`${API_URL}${API.LOG_IN}?redirect=?${QUERY_PARAMETERS.LOGIN_MODULE_REDIRECT}=true`}
          >
            Continue
          </AnchorButton>
        </div>
      </div>
    );
  }
};

export default CTA;
