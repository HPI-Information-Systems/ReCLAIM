import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { JointEvent } from '@/pages/culturalAsset/[id]';
import { getEventProperties } from './getEventProperties';
import { getEventTitle } from './getEventTitle';
import { Entry_str_, TransferEvent } from '@/lib/client';
import { EntryType } from '../../general/types';

function TimelineEvent({
  index,
  numberOfEvents,
  event,
}: {
  index: number;
  numberOfEvents: number;
  event: JointEvent;
}) {
  const eventProperties = getEventProperties(event);
  const title = getEventTitle(event);

  if (eventProperties === null) return null;

  return (
    <div
      style={{
        position: 'relative',
        display: 'flex',
        left: index % 2 == 0 ? '50%' : 0,
        width: '50%',
        marginBottom: '80px',
      }}
    >
      <div
        className="p-5 rounded-md bg-slate-50 shadow flex-grow"
        style={{
          marginRight: index % 2 == 0 ? 0 : '30px',
          marginLeft: index % 2 == 0 ? '30px' : 0,
        }}
      >
        <span className="text-highlight-blue font-bold text-xl">{title}</span>
        {Object.entries(eventProperties).map(([key, eventProperty]) => {
          if (
            eventProperty === null ||
            event[key as keyof JointEvent] === undefined ||
            event[key as keyof JointEvent] === null
          ) {
            return null;
          }

          let values: any[] = [];

          if (
            eventProperty.entityType === EntryType.RELATION &&
            event[key as keyof JointEvent] instanceof Array
          ) {
            values = (event[key as keyof JointEvent]! as any[]).map(
              (relatedEntity, idx) => {
                return (
                  <div key={idx} className="grid grid-cols-3 mt-5">
                    <div className="font-bold mr-3">{eventProperty.label}:</div>
                    <div className="col-span-2">
                      {
                        relatedEntity[eventProperty.displayAttribute!]
                          .parsed as string
                      }
                    </div>
                  </div>
                );
              },
            );
          } else if (eventProperty.entityType === EntryType.RELATION) {
            values = [
              <div key={0} className="grid grid-cols-3 mt-5">
                <div className="font-bold mr-3">{eventProperty.label}:</div>
                <div className="col-span-2">
                  {
                    (event[key as keyof JointEvent] as any)[
                      eventProperty.displayAttribute!
                    ].parsed as string
                  }
                </div>
              </div>,
            ];
          } else {
            values = [
              <div key={0} className="grid grid-cols-3 mt-5">
                <div className="font-bold mr-3">
                  {eventProperty.label as string}:
                </div>
                <div className="col-span-2">
                  {
                    (event[key as keyof JointEvent]! as Entry_str_)
                      .parsed as string
                  }
                </div>
              </div>,
            ];
          }

          return values;
        })}
      </div>
      <div
        className="absolute h-[25px] w-[25px] bg-highlight-blue shadow-xl rounded-[1000px] mt-5"
        style={{
          zIndex: 10,
          right: index % 2 == 0 ? '' : 0,
          transform:
            index % 2 == 0 ? 'translate(-50%, 0)' : 'translate(50%, 0)',
        }}
      ></div>
      {(event.date ||
        (event as TransferEvent).arrival_date ||
        (event as TransferEvent).departure_date) && (
        <div
          className="absolute w-[200px] flex mt-5"
          style={{
            zIndex: 10,
            right: index % 2 == 0 ? '' : -225,
            left: index % 2 == 0 ? -225 : '',
            alignItems: index % 2 == 0 ? 'flex-end' : 'flex-start',
            flexDirection: 'column',
          }}
        >
          <span className="text-xl">
            {(event as TransferEvent).arrival_date
              ? (event as TransferEvent).arrival_date?.parsed
              : event.date
                ? event.date.parsed
                : (event as TransferEvent).departure_date?.parsed}
          </span>
        </div>
      )}
    </div>
  );
}

export default function ProvenanceTimeline({
  events,
}: {
  events: JointEvent[];
}) {
  const [timelineToggled, setTimelineToggled] = useState(false);

  const sortedEvents = events.sort(
    (a, b) => a.relative_order - b.relative_order,
  );

  return (
    <div className="relative mt-10">
      <div
        className="container pt-10 pb-10 shadow-md rounded-lg mt-s10 mb-10 relative overflow-y-hidden"
        style={{
          height: timelineToggled ? 'auto' : 600,
        }}
      >
        <h1 className="text-highlight-blue text-3xl">Known Provenance</h1>
        <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-2 bg-slate-200 rounded-[1000px]"></div>
        <div className="w-full h-full flex-col">
          {sortedEvents.map((event, index) => (
            <TimelineEvent
              key={index}
              index={index}
              numberOfEvents={events.length}
              event={event}
            />
          ))}
        </div>
        <div
          className="absolute transition-opacity z-20 left-0 bottom-0 w-full bottom-0 bg-gradient-to-b from-white to-highlight-blue h-[150px]"
          style={{
            opacity: timelineToggled ? 0 : 0.3,
          }}
        ></div>
      </div>
      <button
        onClick={() => setTimelineToggled(!timelineToggled)}
        className="absolute bottom-0 flex rounded-[1000px] items-center justify-center left-1/2 transform -translate-x-1/2 -translate-y-[-50%] z-30 w-[50px] h-[50px] bg-highlight-blue shadow-xl"
      >
        {timelineToggled ? (
          <ChevronUp color="white" size={40} style={{}} />
        ) : (
          <ChevronDown color="white" size={40} style={{}} />
        )}
      </button>
    </div>
  );
}
