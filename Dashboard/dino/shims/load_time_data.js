// Stand-in for chrome://resources/js/load_time_data.js. Chrome fills these from
// the en-US strings of the offline error page; the game reads only these keys.
// disabledEasterEgg and enableAltGameMode are absent, as on a normal Chrome profile.
const STRINGS = {
  dinoGameA11yAriaLabel: 'Dino game',
  dinoGameA11yDescription:
      'Dino game. A pixelated dinosaur dodges cacti and pterodactyls as it ' +
      'runs across a desolate landscape. When you hear an audio cue, press ' +
      'space to jump over obstacles.',
  dinoGameA11yGameOver: 'Game over, your score is $1.',
  dinoGameA11yHighScore: 'Your highest score is $1.',
  dinoGameA11yJump: 'Jump!',
  dinoGameA11yStartGame: 'Game started.',
  dinoGameA11ySpeedToggle: 'Start slower',
};

export const loadTimeData = {
  valueExists: key => Object.prototype.hasOwnProperty.call(STRINGS, key),
  getValue: key => STRINGS[key],
  getString: key => STRINGS[key],
};
