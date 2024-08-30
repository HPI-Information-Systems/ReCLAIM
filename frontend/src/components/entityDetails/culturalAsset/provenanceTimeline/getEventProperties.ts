import {
  acquisitionEventProperties,
  transferEventProperties,
  confiscationEventProperties,
  depositionEventProperties,
  restitutionEventProperties,
} from './eventProperties';
import { JointEvent } from '@/pages/culturalAsset/[id]';

export function getEventProperties(event: JointEvent) {
  if ('arrival_date' in event) return transferEventProperties;
  if ('deposited_by' in event) return depositionEventProperties;
  if ('acquisition_cost' in event) return acquisitionEventProperties;
  if ('from_legal_entity' in event) return confiscationEventProperties;

  return null;
}
