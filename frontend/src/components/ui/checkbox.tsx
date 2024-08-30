export const Checkbox = ({
  isChecked,
  checkHandler,
  id,
}: {
  isChecked: boolean;
  checkHandler: () => void;
  id: string;
}) => {
  return (
    <div>
      <input
        className="accent-primary"
        type="checkbox"
        id={`checkbox-${id}`}
        checked={isChecked}
        onChange={checkHandler}
      />
    </div>
  );
};
