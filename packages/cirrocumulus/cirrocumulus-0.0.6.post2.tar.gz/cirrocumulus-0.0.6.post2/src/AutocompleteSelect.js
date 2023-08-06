import Chip from '@material-ui/core/Chip';
import MenuItem from '@material-ui/core/MenuItem';
import NoSsr from '@material-ui/core/NoSsr';
import Paper from '@material-ui/core/Paper';
import {withStyles} from '@material-ui/core/styles';
import {emphasize} from '@material-ui/core/styles/colorManipulator';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import CancelIcon from '@material-ui/icons/Cancel';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import React from 'react';

import AsyncSelect from 'react-select/async';

const styles = theme => ({
    root: {
        flexGrow: 1,
    },
    input: {
        display: 'flex',
        padding: 0,
        maxWidth: '220px',
        height: '100%'
    },
    valueContainer: {
        display: 'flex',
        flexWrap: 'wrap',
        flex: 1,
        alignItems: 'center',
        overflow: 'hidden',
    },
    chip: {
        margin: `${theme.spacing(1) / 2}px ${theme.spacing(1) / 4}px`,
    },
    chipFocused: {
        backgroundColor: emphasize(
            theme.palette.type === 'light' ? theme.palette.grey[300] : theme.palette.grey[700],
            0.08,
        ),
    },
    noOptionsMessage: {
        padding: `${theme.spacing(1)}px ${theme.spacing(1) * 2}px`,
    },
    singleValue: {
        fontSize: 16,
    },
    dropdownIndicator: {
        alignSelf: 'flex-end',
        color: 'red'
    },
    placeholder: {
        position: 'absolute',
        left: 2,
        fontSize: 16,
    },
    paper: {
        position: 'absolute',
        zIndex: 1,
        marginTop: theme.spacing(1),
        left: 0,
        right: 0,
    },
    divider: {
        height: theme.spacing(1) * 2,
    },
});

const groupStyles = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
};

const formatGroupLabel = data => (
    <div style={groupStyles}>
        <span>{data.label}</span>
    </div>
);

function NoOptionsMessage(props) {
    return (
        <Typography
            color="textSecondary"
            className={props.selectProps.classes.noOptionsMessage}
            {...props.innerProps}
        >
            {props.children}
        </Typography>
    );
}

function inputComponent({inputRef, ...props}) {
    return <div ref={inputRef} {...props} />;
}

function Control(props) {
    return (
        <TextField
            fullWidth
            InputProps={{
                inputComponent,
                inputProps: {
                    className: props.selectProps.classes.input,
                    inputRef: props.innerRef,
                    children: props.children,
                    ...props.innerProps,
                },
            }}
            {...props.selectProps.textFieldProps}
        />
    );
}

function Option(props) {
    return (
        <MenuItem
            buttonRef={props.innerRef}
            selected={props.isFocused}
            component="div"
            style={{
                fontWeight: props.isSelected ? 500 : 400
            }}
            {...props.innerProps}
        >
            {props.children}
        </MenuItem>
    );
}

function Placeholder(props) {
    return (
        <Typography
            color="textSecondary"
            className={props.selectProps.classes.placeholder}
            {...props.innerProps}
        >
            {props.children}
        </Typography>
    );
}

function SingleValue(props) {
    return (
        <Typography className={props.selectProps.classes.singleValue} {...props.innerProps}>
            {props.children}
        </Typography>
    );
}

function ValueContainer(props) {
    return <div className={props.selectProps.classes.valueContainer}>{props.children}</div>;
}

function MultiValue(props) {
    return (
        <Chip
            tabIndex={-1}
            label={props.children}
            className={classNames(props.selectProps.classes.chip, {
                [props.selectProps.classes.chipFocused]: props.isFocused,
            })}
            onDelete={props.removeProps.onClick}
            deleteIcon={<CancelIcon {...props.removeProps} />}
        />
    );
}

function Menu(props) {
    return (
        <Paper square className={props.selectProps.classes.paper} {...props.innerProps}>
            {props.children}
        </Paper>
    );
}

const components = {
    Control,
    Menu,
    MultiValue,
    NoOptionsMessage,
    Option,
    Placeholder,
    SingleValue,
    ValueContainer
};

class AutocompleteSelect extends React.Component {
    loadOptions = (inputValue, callback) => {
        return callback(this.filterOptions(inputValue));
    };

    noOptionsMessage = () => {
        return 'No matches';
    };

    onChange = (value) => {
        if (this.props.isMulti) {
            this.props.onChange(value == null || value.length === 0 ? null : value.map(item => item.value));
        } else {
            // [value[value.length - 1]]
            this.props.onChange(value);
        }
    };

    onPaste = (event) => {
        let text = event.clipboardData.getData('text/plain');
        if (text != null && text.length > 0) {
            event.preventDefault();
            event.stopPropagation();
            let tokens = text.split(/[\n,]/);
            let results = [];
            tokens.forEach(token => {
                token = token.toLowerCase().trim().replace(/"/g, '');
                if (token !== '') {
                    let found = false;
                    for (let i = 0, ngroups = this.props.options.length; i < ngroups && !found; i++) {
                        let option = this.props.options[i];
                        for (let j = 0, n = option.options.length; j < n; j++) {
                            let choice = option.options[j];
                            if (choice.value.toLowerCase() == token) {
                                results.push(choice.value);
                                break;
                            }
                        }
                    }
                }
            });

            this.props.onChange(results);
        }
    };

    filterOptions = (inputValue) => {
        if (inputValue) {
            inputValue = inputValue.toLowerCase();
            let limit = inputValue.length === 1 ? 3 : (inputValue.length === 2 ? 10 : 20);
            let nmatches = 0;
            let results = [];
            for (let i = 0, ngroups = this.props.options.length; i < ngroups; i++) {
                let option = this.props.options[i];
                let filteredOption = {label: option.label, options: []};
                results.push(filteredOption);
                for (let j = 0, n = option.options.length; j < n; j++) {
                    let choice = option.options[j];
                    if (choice.value.toLowerCase().startsWith(inputValue)) {
                        nmatches++;
                        filteredOption.options.push(choice);
                        if (nmatches === limit) {
                            return results;
                        }
                    }
                }
            }
            return results;
        }
        return [];
    };

    render() {
        const {classes, theme} = this.props;

        const selectStyles = {
            input: base => ({
                ...base,
                color: theme.palette.text.primary,
                '& input': {
                    font: 'inherit',
                },
            }),
        };

        return (
            <div className={classes.root} onPaste={this.onPaste}>
                <NoSsr>
                    <AsyncSelect
                        noOptionsMessage={this.noOptionsMessage}
                        cacheOptions={false}
                        placeholder={''}
                        loadOptions={this.loadOptions}
                        classes={classes}
                        styles={selectStyles}
                        textFieldProps={{
                            label: this.props.label,
                            helperText: this.props.helperText,
                            InputLabelProps: {
                                shrink: true,
                            },
                        }}
                        formatGroupLabel={formatGroupLabel}
                        components={components}
                        onChange={this.onChange}
                        value={this.props.value}
                        isMulti={this.props.isMulti}
                        defaultOptions={this.props.defaultOptions}
                    />
                </NoSsr>
            </div>
        );
    }
}

AutocompleteSelect.propTypes = {
    isMulti: PropTypes.bool.isRequired,
    defaultOptions: PropTypes.array,
    label: PropTypes.string,
    helperText: PropTypes.string,
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired,
    options: PropTypes.array.isRequired,
    onChange: PropTypes.func.isRequired,
};

export default withStyles(styles, {withTheme: true})(AutocompleteSelect);

