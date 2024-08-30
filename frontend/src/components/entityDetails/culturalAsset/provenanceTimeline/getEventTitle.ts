import { JointEvent } from '@/pages/culturalAsset/[id]';

export function getEventTitle(event: JointEvent) {
  if ('arrival_date' in event) return 'Transfer';
  if ('deposited_by' in event) return 'Deposit';
  if ('acquisition_cost' in event) return 'Acquisition';
  if ('from_legal_entity' in event) return 'Confiscation';

  return null;
}
