import { AllAgentConfigsType } from "@/app/types";
import frontDeskAuthentication from "./frontDeskAuthentication";
import customerServiceRetail from "./customerServiceRetail";
import simpleExample from "./simpleExample";
import fastFood from "./fastFood";
import orderAgent from "./fastFood/orderAgent";

export const allAgentSets: AllAgentConfigsType = {
  frontDeskAuthentication,
  customerServiceRetail,
  simpleExample,
  fastFood: [orderAgent],
  default: [orderAgent]
};

export const defaultAgentSetKey = "fastFood";
