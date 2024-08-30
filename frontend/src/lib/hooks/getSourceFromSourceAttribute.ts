import { SupportedSource } from '../client';
import { AVAILABLE_SOURCES } from '../config/sources';

export function getSourceName(source: SupportedSource) {
  for (const available_source in AVAILABLE_SOURCES) {
    if (AVAILABLE_SOURCES[available_source].name === source) {
      return AVAILABLE_SOURCES[available_source].label;
    }
  }
}
