import { Field, Form } from "react-final-form";
import {
  Checkbox,
  DefaultButton,
  Dropdown,
  DropdownMenuItemType,
  IDropdownOption,
  IDropdownStyles,
  ITextFieldStyles,
  Label,
  Stack,
  StackItem,
  TextField,
} from "@fluentui/react";
import axios from "axios";
import { Guid } from "typescript-guid";
import "./RegistrationForm.css";
import React from "react";

const stackTokens = { childrenGap: 50 };
type Status = 'pending' | 'submitted' | 'rejected' | 'accepted'
type RegistrationFormData = {
  appid: string;
  applicationdate: string;
  discordname: string;
  rsiname: string;
  region: string;
  interest: string;
  scstartdate: string;
  expectations: string;
  role: string;
  ships: string;
  refer: string;
  competitive: string;
  pastorgs: string;
  controls: string;
  realworldskills: string;
  strengthsandweakness: string;
  email: string;
  recruiter: string;
  status: Status
};

export const RegistrationForm = () => {
  const onSubmit = React.useCallback(async (values: RegistrationFormData) => {
    //app id
    values.appid = Guid.create().toString();
    //update component to show submitting
    const response = await axios({
      method: 'post',
      url: 'https://viperaveilapi.redshiftent.com/api/vipera/application',
      data: values
    })
    console.log(values);
    console.log(response)
    //update spinner to show submitted
  }, []);

  const [isChecked, setIsChecked] = React.useState(false);
  const onChange = React.useCallback(
    (
      ev?: React.FormEvent<HTMLElement | HTMLInputElement>,
      checked?: boolean
    ): void => {
      setIsChecked(!!checked);
    },
    []
  );
  const dropdownStyles: Partial<IDropdownStyles> = {
    dropdown: { width: 300 },
  };
  const textFieldStyles: Partial<ITextFieldStyles> = {
    fieldGroup: { width: 300 },
  };

  const options: IDropdownOption[] = [
    {
      key: "rolesHeader",
      text: "Roles",
      itemType: DropdownMenuItemType.Header,
    },
    { key: "pilot", text: "Combat Pilot" },
    { key: "fps", text: "Assault Force / Boarding Team" },
    { key: "specialist", text: "Support Specialist" },
  ];
  return (
    <div className="registrationform">
      {/* <Stack tokens={stackTokens} styles={stackStyles}> */}
      <h3>Vipera Veil Application</h3>
      <Label>Application Date {new Date().toLocaleString()}</Label>

      <Form
        onSubmit={onSubmit}
        render={(props) => (
          <form onSubmit={props.handleSubmit}>
            <Stack horizontal tokens={stackTokens}>
              <Field name="discordname">
                {(fieldProps) => (
                  <TextField
                    label="Discord Username"
                    id="discordname"
                    value={fieldProps.input.value}
                    onChange={fieldProps.input.onChange}
                    onBlur={fieldProps.input.onBlur}
                    styles={textFieldStyles}
                    required
                  />
                )}
              </Field>
              <Field name="rsiname">
                {(fieldProps) => (
                  <TextField
                    label="Rsi Username"
                    id="rsiname"
                    value={fieldProps.input.value}
                    onChange={fieldProps.input.onChange}
                    onBlur={fieldProps.input.onBlur}
                    styles={textFieldStyles}
                    required
                  />
                )}
              </Field>
            </Stack>

            <Stack horizontal tokens={{ childrenGap: 31 }}>
              <Field name="role">
                {(fieldProps) => (
                  <Dropdown
                    placeholder="Select a role"
                    label="What type of role would you like to fulfil in the org?"
                    options={options}
                    styles={dropdownStyles}
                    onChange={fieldProps.input.onChange}
                  />
                )}
              </Field>
              <StackItem align="end">
                <Field name="scstartdate">
                  {(fieldProps) => (
                    <TextField
                      label=" What year did you start playing SC?"
                      id="scstartdate"
                      value={fieldProps.input.value}
                      onChange={fieldProps.input.onChange}
                      onBlur={fieldProps.input.onBlur}
                      styles={textFieldStyles}
                      required
                    />
                  )}
                </Field>
              </StackItem>
            </Stack>
            <Field name="region">
              {(fieldProps) => (
                <TextField
                  label="What region are you from? What days & times are you generally available?"
                  id="region"
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>

            <Field name="interest">
              {(fieldProps) => (
                <TextField
                  label="What do you enjoy doing in the verse?"
                  id="interest"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="ships">
              {(fieldProps) => (
                <TextField
                  label="What ships and vehicles do you have in your fleet?"
                  id="ships"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="refer">
              {(fieldProps) => (
                <TextField
                  label="Where did you hear about us & why do you want to join us?"
                  id="refer"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="expectations">
              {(fieldProps) => (
                <TextField
                  label=" What do you expect from this org?"
                  id="expectations"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>

            <Field name="competitive">
              {(fieldProps) => (
                <TextField
                  label=" Are you competitive? (If yes do you have any competitive background?)"
                  id="competitive"
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  multiline
                  resizable={false}
                  required
                />
              )}
            </Field>
            <Field name="pastorgs">
              {(fieldProps) => (
                <TextField
                  label="List your current/past orgs"
                  id="pastorgs"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="controls">
              {(fieldProps) => (
                <TextField
                  label=" What controls do you use? (Mouse & Keyboard, Dual Joysticks, Pedals, Single joystick....?)"
                  id="controls"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="realworldskills">
              {(fieldProps) => (
                <TextField
                  label=" Real-world experience/skills that may be useful for the org?"
                  id="realworldskills"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="strengthsandweakness">
              {(fieldProps) => (
                <TextField
                  label="Tell us about yourself in general, also let us know what are your strengths & weaknesses"
                  id="strengthsandweakness"
                  multiline
                  resizable={false}
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="email">
              {(fieldProps) => (
                <TextField
                  label="Please type your email or gaming email so we give you access to some docs once you're accepted."
                  id="email"
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            <Field name="recruiter">
              {(fieldProps) => (
                <TextField
                  label="Who is your recruiter"
                  id="recruiter"
                  value={fieldProps.input.value}
                  onChange={fieldProps.input.onChange}
                  onBlur={fieldProps.input.onBlur}
                  required
                />
              )}
            </Field>
            
            <Field name="exclusive">
              {(fieldProps) => (
                <div className="controlPadTop">
                <Checkbox
                  label="I acknowledge this is an exclusive organization and my acceptence requires me to leave my previous organizations."
                  id="exclusiveorg"
                  checked={isChecked}
                  onChange={onChange}
                  required
                  
                />
                </div>
              )}
            </Field>
            <DefaultButton type="submit"
            disabled={!isChecked}
            > submit</DefaultButton>
          </form>
        )}
      />
    </div>
  );
};
